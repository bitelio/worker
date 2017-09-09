from copy import copy
import unittest
import datetime
import leankitmocks
from schematics.exceptions import DataError

from ..board import Board
from ..lane import Lane
from ..card import Card
from ..user import User
from ..card_type import CardType
from ..class_of_service import ClassOfService
from ..event import Event


class SchemaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.board = leankitmocks.Board(100000000)
        cls.board.get_archive()

    def test_card(self):
        card = {'AssignedUserId': None, 'BlockReason': '', 'IsBlocked': False,
                'ClassOfServiceId': None, 'TypeId': 100000015, 'Priority': 1,
                'DateArchived': datetime.date(2017, 2, 27), 'Id': 100010003,
                'Description': '', 'DueDate': None, 'ExternalCardID': '',
                'LastActivity': datetime.datetime(2017, 2, 27, 13, 58, 4),
                'LastMove': datetime.datetime(2017, 2, 27, 13, 58, 4),
                'Size': 0, 'Tags': [], 'Title': 'Task 1', 'BoardId': 100000000}
        card['DateArchived'] = datetime.datetime(2017, 2, 27)
        data = Card(self.board.cards[100010003]).to_native()
        self.assertEqual(card, data)

    def test_card_priority(self):
        card = copy(self.board.cards[100010001])
        card['Priority'] = 4
        with self.assertRaises(DataError):
            card = Card(card)

    def test_card_due_date(self):
        card = copy(self.board.cards[100010001])
        del card['DueDate']
        data = Card(card).to_native()
        self.assertTrue('DueDate' in data)

    def test_card_type(self):
        card_type = {'BoardId': 100000000, 'ColorHex': '#ff6c00',
                     'Id': 100000011, 'IsCardType': True,
                     'IsTaskType': True, 'Name': 'Deliverable'}
        data = CardType(self.board.card_types[100000011]).to_native()
        self.assertEqual(card_type, data)

    def test_user(self):
        user = {'BoardId': 100000000, 'Enabled': True, 'FullName': 'User 1',
                'GravatarLink': '36020adab302af77eb6273e0b2ead7cf',
                'Id': 100000001, 'Role': 4, 'UserName': 'User1@example.org'}
        data = User(self.board.users[100000001]).to_native()
        self.assertEqual(user, data)

    def test_class_of_service(self):
        class_of_service = {'BoardId': 100000000, 'ColorHex': '#FFFFFF',
                            'Id': 100000101, 'Title': 'Date Dependent',
                            'UseColor': False}
        data = ClassOfService(self.board.classes_of_service[100000101])
        self.assertEqual(class_of_service, data.to_native())

    def test_board(self):
        board = {'ArchiveTopLevelLaneId': 100001008, 'Title': 'Board 100000000',
                 'TopLevelLaneIds': [100001002, 100001003], 'Id': 100000000,
                 'Version': 16, 'AvailableTags': ['Tag1', 'Tag2'],
                 'BacklogTopLevelLaneId': 100001001, 'Reindex': False}
        data = Board(self.board).to_native()
        self.assertEqual(board, data)

    def test_lane(self):
        lane = {'BoardId': 100000000, 'ChildLaneIds': [], 'Id': 100001001,
                'Index': 0, 'LaneState': 'lane', 'Orientation': 0, 'Width': 1,
                'SiblingLaneIds': [100001002, 100001008, 100001003],
                'ParentLaneId': None, 'Title': 'Backlog'}
        data = Lane(self.board.lanes[100001001]).to_native()
        self.assertEqual(lane, data)

    def test_move_event(self):
        event = {'CardId': 100010003, 'FromLaneId': 100001007,
                 'DateTime': datetime.datetime(2017, 2, 27, 13, 58, 4),
                 'ToLaneId': 100001009, 'Type': 'CardMoveEventDTO',
                 'UserId': 100000001, 'BoardId': 100000000}
        data = Event(self.board.cards[100010003].history[-1]).to_native()
        self.assertEqual(data, event)

    def test_tag_event(self):
        event = {'CardId': 100010001, 'ToLaneId': 100001004,
                 'DateTime': datetime.datetime(2017, 3, 30, 11, 21, 1),
                 'Type': 'CardFieldsChangedEventDTO', 'UserId': 100000001,
                 'Changes': [{'FieldName': 'Tags', 'NewValue': 'Tag1,Tag2',
                              'OldValue': 'Tag1'}], 'BoardId': 100000000}
        data = Event(self.board.cards[100010001].history[-1]).to_native()
        self.assertEqual(data, event)

    def test_comment_event(self):
        event = {'CardId': 100010001, 'CommentText': '<p>Comment 1</p>',
                 'DateTime': datetime.datetime(2017, 2, 27, 13, 58, 15),
                 'Type': 'CommentPostEventDTO', 'UserId': 100000001,
                 'BoardId': 100000000}
        data = Event(self.board.cards[100010001].history[-3]).to_native()
        self.assertEqual(data, event)

    def test_creation_event(self):
        event = {'CardId': 100010002, 'ToLaneId': 100001001,
                 'DateTime': datetime.datetime(2017, 2, 27, 13, 57, 30),
                 'Type': 'CardCreationEventDTO', 'UserId': 100000001,
                 'BoardId': 100000000}
        data = Event(self.board.cards[100010002].history[-1]).to_native()
        self.assertEqual(data, event)
