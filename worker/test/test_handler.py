import leankitmocks

from worker import handler
from worker.test.base import BaseTest
from worker.database import save
from worker.database import load
from worker.database import update
from worker.database import delete


class HandlerTest(BaseTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        save.db = load.db = update.db = delete.db = cls.db
        handler.run(100000000, None)

    def _test_collection_(self, collection):
        expected = len(getattr(self.board, collection))
        actual = self.db[collection].find().count()
        self.assertEqual(expected, actual)


class PopulateTest(HandlerTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.board = leankitmocks.Board(100000000)
        cls.board.get_archive()

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

    def test_board(self):
        self.assertEqual(self.board.id, self.db.boards.find_one()['Id'])


class UpdateTest(HandlerTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.board = leankitmocks.get_newer_if_exists(100000000, 1)
        cls.board.get_archive()
        handler.run(100000000, 1)

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

    def test_board(self):
        expected = self.board.version
        actual = self.db.boards.find_one()['Version']
        self.assertEqual(expected, actual)
