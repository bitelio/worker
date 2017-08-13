#!/usr/bin/python
# -*- coding: utf-8 -*-

from schematics.types import IntType
from schematics.types import ListType
from schematics.types import DictType
from schematics.types import StringType
from schematics.types import DateTimeType

from .models import KanbanModel
from .types import KanbanIdType


class Event(KanbanModel):
    BoardId = KanbanIdType()
    CardId = KanbanIdType()
    Changes = ListType(DictType(StringType))
    DateTime = DateTimeType()
    FromLaneId = KanbanIdType()
    Position = IntType()
    ToLaneId = KanbanIdType()
    Type = StringType()
    UserId = KanbanIdType()
