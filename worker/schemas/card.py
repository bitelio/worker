#!/usr/bin/python
# -*- coding: utf-8 -*-

from schematics.types import IntType
from schematics.types import ListType
from schematics.types import StringType
from schematics.types import BooleanType
from schematics.types import DateTimeType

from . import Model
from .types import KanbanType


class Card(Model):
    Id = KanbanType()
    Title = StringType()
    Description = StringType()
    ExternalCardID = StringType()
    TypeId = KanbanType()
    ClassOfServiceId = KanbanType(required=False)
    AssignedUserId = KanbanType(required=False)
    Priority = IntType(choices=[0, 1, 2, 3])
    Size = IntType()
    Tags = ListType(StringType)
    LastMove = DateTimeType()
    LastActivity = DateTimeType()
    DueDate = DateTimeType()
    DateArchived = DateTimeType()
    IsBlocked = BooleanType()
    BlockReason = StringType()
