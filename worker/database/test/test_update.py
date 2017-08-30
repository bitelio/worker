import leankitmocks

from worker.database import save
from worker.database import delete
from worker.database import update
from worker.schemas.card import Card
from worker.schemas.user import User
from worker.database.test.base import DatabaseTest


class DeleteTest(DatabaseTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        update.db = save.db = delete.db = cls.db
        cls.board = leankitmocks.Board(100000000)

    def test_update_one(self):
        user = self.board.users[100000001]
        self.db.users.insert_one(User(user).to_native())
        user['FullName'] = 'Test User'
        update.one(user)
        expected = User(user).to_native()
        actual = self.db.users.find_one({'Id': 100000001}, {'_id': 0})
        self.assertEqual(expected, actual)

    def test_update_card(self):
        card = self.board.cards[100010001]
        self.db.cards.insert_one({'Id': 100010001})
        self.db.events.insert_many([{'CardId': 100010001}])
        update.card(card)
        expected = Card(card).to_native()
        actual = self.db.cards.find_one({'Id': 100010001}, {'_id': 0})
        self.assertEqual(expected, actual)
        expected = len(card.history)
        actual = self.db.events.find({'CardId': 100010001}).count()
        self.assertEqual(expected, actual)
