#!/usr/bin/python
# -*- coding: utf-8 -*-

from schematics.types import ListType
from schematics.types import IntType
from schematics.types import StringType

from . import Model
from .types import KanbanType


class Board(Model):
    Id = KanbanType()
    Title = StringType()
    Version = IntType()
    TopLevelLaneIds = ListType(KanbanType)
    BacklogTopLevelLaneId = IntType()
    ArchiveTopLevelLaneId = IntType()
    AvailableTags = ListType(StringType)
