#!/usr/bin/python
# -*- coding: utf-8 -*-

from schematics.types import IntType
from schematics.types import ListType
from schematics.types import DateType
from schematics.types import StringType
from schematics.types import BooleanType
from schematics.types import DateTimeType

from .models import KanbanModel
from .types import KanbanIdType


class Card(KanbanModel):
    AssignedUserId = KanbanIdType(required=False)
    BlockReason = StringType()
    BoardId = KanbanIdType()
    ClassOfServiceId = KanbanIdType(required=False)
    DateArchived = DateType(required=False)
    Description = StringType()
    DueDate = DateType(required=False)
    ExternalCardID = StringType()
    Id = KanbanIdType()
    IsBlocked = BooleanType()
    LastActivity = DateTimeType()
    LastMove = DateTimeType()
    Priority = IntType(choices=[0, 1, 2, 3])
    Size = IntType()
    Tags = ListType(StringType)
    Title = StringType()
    TypeId = KanbanIdType()
