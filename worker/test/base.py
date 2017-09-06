import unittest
import mongomock

from worker.database import mongo


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = mongomock.MongoClient()
        cls.db = cls.client.test
        mongo.db = cls.db

    @classmethod
    def tearDownClass(cls):
        cls.client.drop_database('test')
