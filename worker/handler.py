import logging
import leankit
from officehours import Calculator
from pymongo.errors import DuplicateKeyError

from . import config
from . import mappings
from . import database


log = logging.getLogger(__name__)


class Updater:
    def __init__(self, board, version, archive=False):
        self.board_id = board['Id']
        self.version = version
        self.archive = archive
        self.timer = Calculator(*board['OfficeHours'], board['Holidays'])

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
        log.debug(f'Checking board {self.board_id} for updates')
        arguments = self.board_id, self.version, config.TIMEZONE
        self.board = leankit.get_newer_if_exists(*arguments)
        if self.board:
            log.debug(f'Updating board {self.board_id} to v{self.version}')
            if self.archive:
                self.board.get_archive()
            board = database.load.one('boards', self.board_id)
            if not self.equal(board, self.board):
                database.update.one(self.board)
            self.update_collections()
            self.update_cards()
            self.version = self.board.version

    def populate(self):
        log.info(f'Populating board {self.board_id}')
        self.board = leankit.Board(self.board_id, config.TIMEZONE)
        self.board.get_archive()
        database.save.one(self.board)
        types = ['lanes', 'cards', 'users', 'card_types', 'classes_of_service']
        for collection in types:
            database.save.many(getattr(self.board, collection).values())
        cards = self.board.cards.values()
        events = [events for card in cards
                  for events in self.intervals(card.history)]
        database.save.many(events)
        self.version = self.board.version

    def update_collections(self):
        collections = ['lanes', 'users', 'card_types', 'classes_of_service']
        query = {'BoardId': self.board_id}
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
        query = {'BoardId': self.board_id, 'DateArchived': None}
        options = {'query': query, 'timezone': config.TIMEZONE}
        cards = database.load.table('cards', **options)
        for card_id, card in self.board.cards.items():
            if card_id not in cards:
                card.history = self.intervals(card.history)
                try:
                    database.save.card(card)
                except DuplicateKeyError:
                    log.warning(f'Card {card_id} found as duplicate')
                    database.update.card(card)
            else:
                last_activity = cards[card_id]['LastActivity']
                if card['LastActivity'] != last_activity:
                    events = self.intervals(card.history, last_activity)
                    database.update.card(card, events)

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
                        last_activity = cards[card_id]['LastActivity']
                        events = self.intervals(card.history, last_activity)
                        database.update.card(card, events)
                except ConnectionError:
                    database.delete.card(card_id)

    def intervals(self, history, last_activity=None):
        """ Calculate the TRT for each move card event. Last one has no TRT """
        previous = history[0]
        if previous['Type'] != 'CardCreationEventDTO':
            log.error(f"Card {card.id} didn't start with a creation event")
        events = [] if last_activity else [previous]
        for event in history[1:]:
            if event['Type'] == 'CardMoveEventDTO':
                time_delta = event['DateTime'] - previous['DateTime']
                interval = (previous['DateTime'], event['DateTime'])
                previous['TimeDelta'] = time_delta.total_seconds()
                previous['TRT'] = self.timer.working_seconds(*interval)
                previous = event
            if not last_activity or event['DateTime'] > last_activity:
                events.append(event)
        return events


def run(board, version, archive=False):
    updater = Updater(board, version, archive)
    updater.run()
    return updater.version
