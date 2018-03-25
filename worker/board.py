import leankit
from datetime import timedelta
from structlog import get_logger
from officehours import Calculator
from schematics.models import Model
from schematics.exceptions import DataError

from . import env
from .utils import lock
from .mappings import items, collections
from .schemas.card import Card, Event
from .schemas.board import Board


class Updater:
    def __init__(self, board_id: int) -> None:
        self.log = get_logger(f"worker.{board_id}").bind(board=board_id)
        self.version: int = 0
        self.hashes: dict = {}
        self.id: int = board_id
        self.reload()
        self.download()

    def download(self):
        self.log.info("Downloading board", action="download")
        board = leankit.Board(self.id, self.timezone)
        card_ids = list(board.cards.keys())
        board.get_archive()
        for card in board.cards.values():
            self.log.debug("Downloading card", action="download", id=card.id,
                           info=len(card.history), type="card")
        with lock(f"read:{board.id}"):
            self.reset()
            data = Board(board).to_native()
            env.db.boards.update_one({"Id": self.id}, {"$set": data})
            try:
                for item in items:
                    units = getattr(board, item.collection).values()
                    if units:
                        models = [item.schema(unit) for unit in units]
                        data = [model.to_native() for model in models]
                        env.db[item.collection].insert_many(data)
                        hashes = {model["Id"]: model.hash for model in models}
                        self.hashes[item.collection] = hashes
                events = [event for card in board.cards.values()
                          for event in self.history(card.history)]
                env.db.events.insert_many(events)
            except DataError as error:
                self.log.error(f"{item.card} data error",
                               type=item.variable, error=error)
                self.reset()
                raise error
            cards = {card: board.cards[card].version for card in card_ids}
            self.hashes["cards"] = cards

    def update(self):
        arguments = self.id, self.version, self.timezone
        self.log.debug("Updating board", action="update")
        board = leankit.get_newer_if_exists(*arguments)
        if board:
            data = Board(board).to_native()
            env.db.boards.update_one({"Id": self.id}, {"$set": data})
            for item in items:
                log = self.log.bind(type=item.variable)
                units = getattr(board, item.collection)
                hashes = self.hashes[item.collection]
                for item_id, data in units.items():
                    log = log.bind(id=item_id)
                    try:
                        model = item.schema(data)
                    except DataError as error:
                        log.error("{item.card} data error", error=error)
                        continue

                    if item_id not in hashes:
                        try:
                            self.insert(model, item.collection)
                            log.info(f"{item.name} created", action="create")
                        except env.DuplicateKeyError:
                            log.error("Duplicate {item.name} found",
                                      error="duplicate")
                    elif model.hash != hashes[item_id]:
                        log.info(f"{item.name} updated", action="update")
                        self.replace(model, item.collection)

                cached_ids = list(hashes.keys())
                for item_id in cached_ids:
                    if item_id not in units:
                        log = log.bind(id=item_id)
                        if item.collection == "cards":
                            try:
                                card = board.get_card(item_id)
                            except ConnectionError:
                                pass
                            else:
                                if card.lane:
                                    self.info(f"{item.name} archived",
                                              action="archive")
                                    model = item.schema(card)
                                    self.replace(model, item.collection)
                                    continue
                        log.info(f"{item.name} deleted", action="delete")
                        self.delete(item_id, item.collection)

            self.version = board.version

    def insert(self, model: Model, collection: str):
        if isinstance(model, Card):
            history = model.card.history
            with lock(f"read:{self.id}"):
                try:
                    events = self.history(history)
                except DataError as error:
                    self.log.error("History data error", error=error,
                                   id=model.Id, type="card")
                    return
                env.db.events.insert_many(events)
                env.db.cards.insert_one(model.to_native())
        else:
            env.db[collection].insert_one(model.to_native())
        self.hashes[collection][model.Id] = model.hash

    def replace(self, model: Model, collection: str):
        if isinstance(model, Card):
            history = model.card.history
            with lock(f"read:{self.id}"):
                env.db.events.delete_many({"CardId": model.Id})
                try:
                    events = self.history(history)
                except DataError as error:
                    self.log.error("History data error", error=error,
                                   id=model.Id, type="card")
                    env.db.cards.delete_one({"Id": model.Id})
                    return
                env.db.events.insert_many(events)
                env.db.cards.replace_one({"Id": model.Id}, model.to_native())
        else:
            env.db[collection].replace_one({"Id": model.Id}, model.to_native())
        self.hashes[collection][model.Id] = model.hash

    def delete(self, item_id: int, collection: str):
        if collection == "cards":
            env.db.events.delete_many({"CardId": item_id})
        env.db[collection].delete_one({"Id": item_id})
        del self.hashes[collection][item_id]

    def reset(self):
        self.log.info("Resetting board", action="reset")
        for collection in collections:
            env.db[collection].delete_many({"BoardId": self.id})
        env.db.events.delete_many({"BoardId": self.id})

    def reload(self):
        conf = env.db.boards.find_one({"Id": self.id})
        self.timer = Calculator(*conf["OfficeHours"], conf["Holidays"])
        self.timezone = conf["Timezone"]

    def history(self, history: list):
        if history[0]["Type"] != "CardCreationEventDTO":
            card_id = history[0]["CardId"]
            date_format = "%m/%d/%Y at %I:%M:%S %p"
            one_second = timedelta(seconds=1)
            log = self.log.bind(id=card_id, type="card")
            for i, event in enumerate(history[1:]):
                if event["Type"] == "CardCreationEventDTO":
                    creation = history.pop(i+1)
                    mismatch = creation["DateTime"] - history[0]["DateTime"]
                    seconds = int(mismatch.total_seconds())
                    log.warning("Date mismatch", info=seconds)
                    date_time = history[0]["DateTime"] - one_second
                    creation["DateTime"] = date_time.strftime(date_format)
                    history.insert(0, creation)
                    break
            else:
                log.warning("No creation date")

        previous = None
        for event in history:
            event["BoardId"] = self.id
            if event["Type"] in ["CardMoveEventDTO", "CardCreationEventDTO"]:
                if previous:
                    time_delta = event["DateTime"] - previous["DateTime"]
                    interval = (previous["DateTime"], event["DateTime"])
                    previous["TimeDelta"] = time_delta.total_seconds()
                    previous["TRT"] = self.timer.working_seconds(*interval)
                previous = event

        return [Event(event).to_native() for event in history]
