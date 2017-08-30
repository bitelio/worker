from copy import deepcopy

from worker.database.test.base import DatabaseTest
from worker.database import load


class LoadTest(DatabaseTest):
    data = [{'Id': 1, 'Color': True}, {'Id': 2, 'Color': False}]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load.db = cls.db
        load.db.items.insert_many(deepcopy(cls.data))

    def test_load_one(self):
        self.assertEqual(self.data[0], load.one('items', 1))

    def test_load_one_missing(self):
        self.assertEqual(None, load.one('items', 0))

    def test_load_many(self):
        self.assertEqual(self.data, load.many('items'))

    def test_load_many_with_query(self):
        self.assertEqual([self.data[1]], load.many('items', {'Color': False}))

    def test_load_many_with_projection(self):
        expected = [{'Id': 1}, {'Id': 2}]
        actual = load.many('items', projection={'Id': 1})
        self.assertEqual(expected, actual)

    def test_load_field(self):
        self.assertEqual([1, 2], load.field('items'))

    def test_load_field_color(self):
        self.assertEqual([True, False], load.field('items', 'Color'))

    def test_load_field_with_query(self):
        self.assertEqual([1], load.field('items', query={'Id': 1}))

    def test_load_table(self):
        expected = {item['Id']: item for item in self.data}
        actual = load.table('items')
        self.assertEqual(expected, actual)

    def test_load_table_color(self):
        expected = {item['Color']: item for item in self.data}
        actual = load.table('items', 'Color')
        self.assertEqual(expected, actual)

    def test_load_table_with_query_and_projection(self):
        expected = {1: {'Id': 1}}
        actual = load.table('items', query={'Id': 1}, projection={'Id': 1})
        self.assertEqual(expected, actual)
