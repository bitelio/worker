import unittest
import leankitmocks

from worker.schemas.board import Board


class SchemaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.board = leankitmocks.Board(100000000)
        cls.board.get_archive()

    def test_board(self):
        board = {'ArchiveTopLevelLaneId': 100001008, 'Id': 100000000,
                 'TopLevelLaneIds': [100001002, 100001003], 'Version': 16,
                 'AvailableTags': ['Tag1', 'Tag2'], 'Title': 'Board 100000000',
                 'BacklogTopLevelLaneId': 100001001}
        data = Board(self.board).to_native()
        self.assertEqual(board, data)
