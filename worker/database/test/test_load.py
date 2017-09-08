from copy import deepcopy
from pytz import timezone
from datetime import datetime

from worker.database import load
from worker.test.base import BaseTest


class LoadTest(BaseTest):
    data = [{'Id': 2, 'Color': False}, {'Id': 1, 'Color': True}]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.db.items.insert_many(deepcopy(cls.data))

    def test_load_one(self):
        self.assertEqual(self.data[1], load.one('items', 1))

    def test_load_one_missing(self):
        self.assertEqual(None, load.one('items', 0))

    def test_load_many(self):
        actual = load.many('items')
        self.assertIn(self.data[0], actual)
        self.assertIn(self.data[1], actual)

    def test_load_many_with_query(self):
        self.assertEqual([self.data[0]], load.many('items', {'Color': False}))

    def test_load_many_with_projection(self):
        items = [{'Id': 1}, {'Id': 2}]
        actual = load.many('items', projection={'Id': 1})
        self.assertIn(items[0], actual)
        self.assertIn(items[1], actual)

    def test_load_field(self):
        self.assertIn(1, load.field('items'))
        self.assertIn(2, load.field('items'))

    def test_load_field_color(self):
        actual = load.field('items', 'Color')
        self.assertIn(True, actual)
        self.assertIn(False, actual)

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

    def test_load_with_timezone(self):
        date = datetime(2017, 12, 31)
        local = timezone('Europe/Berlin').localize(date)
        self.db.dates.insert_one({'Id': 1, 'Date': local})
        actual = load.one('dates', 1, 'Europe/Berlin')['Date']
        self.assertEqual(str(local), str(actual))
        # The following test doesn't seem to work with mongomock
        # actual = load.one('dates', 1)['Date']
        # self.assertEqual(str(date), str(actual))

    def test_load_without_timezone(self):
        date = datetime(2017, 12, 31)
        self.db.dates.insert_one({'Id': 2, 'Date': date})
        actual = load.one('dates', 2, 'Europe/Berlin')['Date']
        self.assertEqual(str(date), str(actual))

    def test_load_sorted(self):
        expected = [{'Id': 1}, {'Id': 2}]
        actual = load.many('items', projection={'Id': 1}, sort='Id')
        self.assertEqual(expected, actual)
