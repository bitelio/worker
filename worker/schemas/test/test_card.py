#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import copy
import unittest
import datetime
import leankitmocks
from schematics.exceptions import DataError

from ..card import Card


class CardTest(unittest.TestCase):
    @classmethod
    def setUp(self):
        board = leankitmocks.Board(100000000)
        board.get_archive()
        self.card = board.cards[100010003]

    def test_schema(self):
        card = {'AssignedUserId': None, 'BlockReason': '', 'IsBlocked': False,
                'ClassOfServiceId': None, 'TypeId': 100000015, 'Priority': 1,
                'DateArchived': datetime.date(2017, 2, 27), 'Id': 100010003,
                'Description': '', 'DueDate': None, 'ExternalCardID': '',
                'LastActivity': datetime.datetime(2017, 2, 27, 13, 58, 4),
                'LastMove': datetime.datetime(2017, 2, 27, 13, 58, 4),
                'Size': 0, 'Tags': [], 'Title': 'Task 1', 'BoardId': 100000000}
        data = Card(self.card).to_native()
        self.assertEqual(card, data)

    def test_priority(self):
        card = copy(self.card)
        card.priority = 4
        with self.assertRaises(DataError):
            card = Card(card)
