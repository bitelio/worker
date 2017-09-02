import logging
import leankit
from pymongo.errors import DuplicateKeyError

from . import schemas
from . import mappings
from .database import save
from .database import load
from .database import update
from .database import delete

from pprint import pprint

log = logging.getLogger(__name__)


class Updater:
    def __init__(self, board_id, version):
        self.board_id = board_id
        self.id = board_id
        self.version = version
        self.archive = False

    def log(self, item, event):
        name = mappings.get('name', item)
        log.info(f'{name} {event} {item} ({item.id})')

    def run(self):
        # TODO: lock file
        if self.version:
            self.update()
        else:
            self.populate()
        # release lock file

    def convert(self, item):
        if isinstance(item, leankit.kanban.Converter):
            return mappings.get('schema', item)(item).to_native()
        elif isinstance(item, dict):
            return item
        else:
            raise ValueError(f'{type(item)} is not a valid type for conversion')

    def equal(self, one, two):
        first = self.convert(one)
        second = self.convert(two)
        if first.keys() != second.keys():
            return False
        for key, val in first.items():
            if second[key] != val:
                log.debug(f'{key}: {val} --> {second[key]}')
                return False
        return True

    def update(self):
        self.board = leankit.get_newer_if_exists(self.id, self.version)
        board = load.one('boards', self.board.id)
        if self.board:
            if not self.equal(board, self.board):
                update.one(self.board)
            self.update_collections()
            self.update_cards()

    def populate(self):
        print('-'*40)
        self.board = leankit.Board(self.board_id)
        self.board.get_archive()
        self.archive = True
        save.one(self.board)
        types = ['lanes', 'cards', 'users', 'card_types', 'classes_of_service']
        for collection in types:
            save.many(getattr(self.board, collection).values())
        cards = self.board.cards.values()
        events = [events for card in cards for events in card.history]
        save.many(events)

    def update_collections(self):
        collections = ['lanes', 'users', 'card_types', 'classes_of_service']
        query = {'BoardId': self.board.id}
        for collection in collections:
            items = load.table(collection, query=query)
            for item_id, item in getattr(self.board, collection).items():
                if item_id not in items:
                    save.one(item)
                elif not self.equal(items[item_id], item):
                    update.one(item)
            for item_id in items:
                if item_id not in getattr(self.board, collection):
                    delete.one(collection, item_id)

    def update_cards(self):
        query = {'BoardId': self.board.id, 'DateArchived': None}
        cards = load.table('cards', query=query)
        for card_id, card in self.board.cards.items():
            if card_id not in cards:
                try:
                    save.card(card)
                except DuplicateKeyError:
                    update.card(card)
            else:
                if card['LastActivity'] != cards[card_id]['LastActivity']:
                    update.card(card)

        for card_id in cards:
            if card_id not in self.board.cards:
                archived = self.board.get_card(card_id)
                if archived:
                    # Remove when Leankit fixes bug 111106
                    del archived['ActualStartDate']
                    del archived['ActualFinishDate']
                    # ------------------------------------
                    update.card(archived)
                else:
                    delete.card(card_id)


def run(board_id, version):
    updater = Updater(board_id, version)
    updater.run()
