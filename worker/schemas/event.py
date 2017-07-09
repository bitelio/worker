#!/usr/bin/python
# -*- coding: utf-8 -*-

from schematics.types import IntType
from schematics.types import ListType
from schematics.types import DictType
from schematics.types import StringType
from schematics.types import DateTimeType

from . import Model
from .types import KanbanType


class Event(Model):
    Type = StringType()
    CardId = KanbanType()
    UserId = KanbanType()
    Position = IntType()
    DateTime = DateTimeType()
    ToLaneId = KanbanType()
    FromLaneId = KanbanType()
    Changes = ListType(DictType)
