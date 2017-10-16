import logging
import leankit
from datetime import timedelta
from officehours import Calculator
from pymongo.errors import DuplicateKeyError

from . import config, mappings, database


log = logging.getLogger(__name__)


class Updater:
    def __init__(self, board, version, archive=False):
        self.board_id = board['Id']
        self.version = version
        self.archive = archive
        self.timer = Calculator(*board['OfficeHours'], board['Holidays'])

    def run(self):
        # TODO: lock file
        self.stage()
        if self.version:
            self.update()
        else:
            self.populate()
        # release lock file

    def stage(self):
        """ Add stage field to lanes """
        for lane in self.board.archive_lanes:
            lane['Stage'] = 'archive'
        for lane in self.board.backlog_lanes:
            lane['Stage'] = 'backlog'

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
        query = {'BoardId': self.board_id}
        if not self.archive:
            query['DateArchived'] = None
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
                if card['LastActivity'] != cards[card_id]['LastActivity']:
                    card.history = self.intervals(card.history)
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
                        card.history = self.intervals(card.history)
                        database.update.card(card)
                except ConnectionError:
                    database.delete.card(card_id)

    def intervals(self, history):
        """ Calculate the TRT for each move card event. Last one has no TRT """
        history = self.fix_history(history)
        previous = None
        events = []
        for event in history:
            if event['Type'] in ['CardMoveEventDTO', 'CardCreationEventDTO']:
                if previous:
                    time_delta = event['DateTime'] - previous['DateTime']
                    interval = (previous['DateTime'], event['DateTime'])
                    previous['TimeDelta'] = time_delta.total_seconds()
                    previous['TRT'] = self.timer.working_seconds(*interval)
                previous = event
            events.append(event)
        return events

    @staticmethod
    def fix_history(history):
        """ For some cards, the creation event is not the first event """
        if history[0]['Type'] == 'CardCreationEventDTO':
            return history
        else:
            one_second = timedelta(seconds=1)
            date_format = '%d/%m/%Y at %I:%M:%S %p'
            for i, event in enumerate(history[1:]):
                if event['Type'] == 'CardCreationEventDTO':
                    creation = history.pop(i+1)
                    mismatch = creation['DateTime'] - history[0]['DateTime']
                    log.warning(f'Date mismatch: {mismatch.total_seconds()}s')
                    date_time = history[0]['DateTime'] - one_second
                    creation['DateTime'] = date_time.strftime(date_format)
                    history.insert(0, creation)
                    break
            else:
                card_id = history[0]['CardId']
                log.warning(f'Card {card_id} has no creation date')
            return history


def run(board, version, archive=False):
    updater = Updater(board, version, archive)
    updater.run()
    return updater.version
