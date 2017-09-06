from worker.database import delete
from worker.test.base import BaseTest


class DeleteTest(BaseTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_delete_one(self):
        self.db.things.insert_one({'Id': 1})
        delete.one('things', 1)
        self.assertEqual(None, self.db.things.find_one())

    def test_delete_many(self):
        self.db.items.insert_many([{'Id': i} for i in range(10)])
        delete.many('items', {})
        self.assertEqual(None, self.db.items.find_one())

    def test_delete_many_with_query(self):
        self.db.items.insert_many([{'Id': i} for i in range(10)])
        delete.many('items', {'Id': {'$gt': 5}})
        self.assertEqual(6, self.db.items.find().count())

    def test_delete_card(self):
        cards = [{'Id': i} for i in range(3)]
        events = [{'CardId': i, 'Id': j} for i in range(3) for j in range(3)]
        self.db.cards.insert_many(cards)
        self.db.events.insert_many(events)
        delete.card(1)
        self.assertEqual(2, self.db.cards.find().count())
        self.assertEqual(6, self.db.events.find().count())
