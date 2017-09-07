import logging
import leankit
from pymongo.errors import DuplicateKeyError

from . import config
from . import mappings
from . import database


log = logging.getLogger(__name__)


class Updater:
    def __init__(self, board_id, version):
        self.board_id = board_id
        self.id = board_id
        self.version = version
        self.timezone = config.TIMEZONE

    def run(self):
        # TODO: lock file
        if self.version:
            self.update()
        else:
            self.populate()
        # release lock file

    @staticmethod
    def convert(item):
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
        log.debug(f'Checking board {self.id} for updates')
        arguments = self.id, self.version, self.timezone
        self.board = leankit.get_newer_if_exists(*arguments)
        if self.board:
            log.debug(f'Updating board {self.board.id} to v{self.version}')
            board = database.load.one('boards', self.board.id)
            if not self.equal(board, self.board):
                database.update.one(self.board)
            self.update_collections()
            self.update_cards()
            self.version = self.board.version

    def populate(self):
        log.info(f'Populating board {self.id}')
        self.board = leankit.Board(self.board_id, self.timezone)
        self.board.get_archive()
        database.save.one(self.board)
        types = ['lanes', 'cards', 'users', 'card_types', 'classes_of_service']
        for collection in types:
            database.save.many(getattr(self.board, collection).values())
        cards = self.board.cards.values()
        events = [events for card in cards for events in card.history]
        database.save.many(events)
        self.version = self.board.version

    def update_collections(self):
        collections = ['lanes', 'users', 'card_types', 'classes_of_service']
        query = {'BoardId': self.board.id}
        for collection in collections:
            items = database.load.table(collection, query=query)
            for item_id, item in getattr(self.board, collection).items():
                if item_id not in items:
                    database.save.one(item)
                elif not self.equal(items[item_id], item):
                    database.update.one(item)
            for item_id in items:
                if item_id not in getattr(self.board, collection):
                    database.delete.one(collection, item_id)

    def update_cards(self):
        query = {'BoardId': self.board.id, 'DateArchived': None}
        options = {'query': query, 'timezone': self.timezone}
        cards = database.load.table('cards', **options)
        for card_id, card in self.board.cards.items():
            if card_id not in cards:
                try:
                    database.save.card(card)
                except DuplicateKeyError:
                    log.warning(f'Card {card_id} found as duplicate')
                    database.update.card(card)
            else:
                if card['LastActivity'] != cards[card_id]['LastActivity']:
                    database.update.card(card)

        for card_id in cards:
            if card_id not in self.board.cards:
                try:
                    card = self.board.get_card(card_id)
                    if card.lane:
                        # If it doesn't have a lane, the card has become a task
                        # Remove when Leankit fixes bug 111106
                        del card['ActualStartDate']
                        del card['ActualFinishDate']
                        # ------------------------------------
                        database.update.card(card)
                except ConnectionError:
                    database.delete.card(card_id)


def run(board_id, version):
    updater = Updater(board_id, version)
    updater.run()
    return updater.version
