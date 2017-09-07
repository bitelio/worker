import leankitmocks

from worker.test.base import BaseTest


class MockTest(BaseTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.board = leankitmocks.Board(100000000)
