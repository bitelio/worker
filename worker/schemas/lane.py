#!/usr/bin/python
# -*- coding: utf-8 -*-

from schematics.types import IntType
from schematics.types import ListType
from schematics.types import StringType

from . import Model
from . import KanbanIdType


class Lane(Model):
    Id = KanbanIdType(required=True)
    Title = StringType(required=True)
    Index = IntType(required=True)
    Width = IntType(required=True)
    Orientation = IntType(required=True)
    ParentLaneId = KanbanIdType(required=True)
    ChildLaneIds = ListType(KanbanIdType, required=True)
    SiblingLaneIds = ListType(KanbanIdType, required=True)
    LaneState = StringType(required=True)
    BoardId = KanbanIdType(required=True)
