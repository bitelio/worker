from schematics.exceptions import DataError

from worker.database import save
from worker.schemas.card import Card
from worker.schemas.user import User
from .mock import MockTest


class SaveTest(MockTest):
    def test_save_one(self):
        user = self.board.users[100000001]
        save.one(user)
        expected = User(user).to_native()
        actual = self.db.users.find_one({}, {'_id': 0})
        self.assertEqual(expected, actual)

    def test_save_one_and_fail(self):
        card = self.board.cards[100010001]
        card['Id'] = 123
        with self.assertRaises(DataError):
            save.one(card)

    def test_save_many(self):
        save.many(self.board.lanes.values())
        self.assertEqual(10, self.db.lanes.find().count())

    def test_save_many_and_fail(self):
        self.board.card_types[100000013]['Name'] = False
        with self.assertRaises(DataError):
            save.many(self.board.card_types.values())
        self.assertEqual(0, self.db.card_types.find().count())

    def test_save_settings(self):
        save.settings([self.board])
        self.assertEqual(1, self.db.settings.find().count())

    def test_save_card(self):
        card = self.board.cards[100010002]
        save.card(card)
        expected = Card(card).to_native()
        actual = self.db.cards.find_one({'Id': 100010002}, {'_id': 0})
        self.assertEqual(expected, actual)
        self.assertEqual(1, self.db.events.find({'CardId': 100010002}).count())

    # TODO: test duplication error
