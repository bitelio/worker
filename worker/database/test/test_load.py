import unittest
import mongomock
import leankitmocks

from worker.database import load
from worker.database import save
from worker.schemas.board import Board


class DatabaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = mongomock.MongoClient()
        load.db = save.db = cls.client.test
        cls.board = leankitmocks.Board(100000000)
        save.one(cls.board)
        save.many(cls.board.lanes.values())

    @classmethod
    def tearDownClass(cls):
        cls.client.drop_database('test')

    def test_load_one(self):
        data = Board(self.board).to_native()
        self.assertEqual(data, load.one('boards', 100000000))

    def test_load_one_and_fail(self):
        self.assertEqual(None, load.one('boards', 000000000))

    def test_load_many(self):
        data = load.many('lanes', {'BoardId': 100000000})
        self.assertEqual(10, len(data))
        self.assertEqual(10, len(data[0].keys()))
        data = load.many('lanes', {'BoardId': 100000000}, {'Id': 1})
        self.assertEqual(1, len(data[0].keys()))

    def test_load_field(self):
        self.assertEqual([100000000], load.field('boards', 'Id'))

    def test_load_table(self):
        data = Board(self.board).to_native()
        self.assertEqual({100000000: data}, load.table('boards'))
