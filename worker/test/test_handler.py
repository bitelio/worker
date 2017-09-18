import datetime
import leankitmocks
import unittest

from worker import handler
from worker.test.base import BaseTest


class PopulateTest(BaseTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.proto = {'Id': 100000000, 'OfficeHours': ['8:00', '16:00'],
                     'Holidays': [datetime.datetime(2017, 3, 1)]}
        handler.run(cls.proto, None)
        cls.board = leankitmocks.Board(100000000)
        cls.board.get_archive()

    def _test_collection_(self, collection):
        expected = len(getattr(self.board, collection))
        actual = self.db[collection].find().count()
        self.assertEqual(expected, actual)

    def test_cards(self):
        self._test_collection_('cards')

    def test_lanes(self):
        self._test_collection_('lanes')

    def test_users(self):
        self._test_collection_('users')

    def test_card_types(self):
        self._test_collection_('card_types')

    def test_classes_of_service(self):
        self._test_collection_('classes_of_service')

    def test_events(self):
        cards = self.board.cards.values()
        expected = len([event for card in cards for event in card.history])
        actual = self.db.events.find().count()
        self.assertEqual(expected, actual)

    def test_event_trt(self, times=None):
        cards = times or {
            100010001: [19800, 19800, None, None, None, None, None],
            100010002: [None],
            100010003: [0, 0, 18000, 28800, 28800, None]
        }
        for card_id in cards:
            cursor = self.db.events.find({'CardId': card_id}).sort('DateTime')
            events = list(cursor.sort('DateTime'))
            for i, event in enumerate(events):
                self.assertEqual(cards[card_id][i], event.get('TRT'))

    def test_board(self):
        self.assertEqual(self.board.id, self.db.boards.find_one()['Id'])


class UpdateTest(PopulateTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.board = leankitmocks.get_newer_if_exists(100000000, 1)
        cls.board.get_archive()
        handler.run(cls.proto, 1)

    def test_board(self):
        expected = self.board.version
        actual = self.db.boards.find_one()['Version']
        self.assertEqual(expected, actual)

    def test_event_trt(self, times=None):
        trt = {
            100010001: [19800, 19800, None, 305100, None, None, None, None],
            100010002: [140400, None],
            100010003: [0, 0, 18000, 28800, 28800, None],
            100010004: [None]
        }
        super().test_event_trt(trt or times)


class StaticTest(unittest.TestCase):
    def test_fix_history(self):
        history = [
            {'CardId': 123456789, 'Type': 'CardMoveEventDTO',
             'DateTime': datetime.datetime(2017, 1, 1, 12)},
            {'CardId': 123456789, 'Type': 'CardCreationEventDTO',
             'DateTime': datetime.datetime(2017, 1, 1, 12, 1)},
        ]
        actual = handler.Updater.fix_history([event for event in history])
        history[1]['DateTime'] = datetime.datetime(2017, 1, 1, 11, 59, 59)
        expected = history[::-1]
        self.assertEqual(expected, actual)
