import unittest
import mongomock


class DatabaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = mongomock.MongoClient()
        cls.db = cls.client.test

    @classmethod
    def tearDownClass(cls):
        cls.client.drop_database('test')
