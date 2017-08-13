#!/usr/bin/python
# -*- coding: utf-8 -*-

from schematics.types import StringType
from schematics.types import BooleanType

from .models import KanbanModel
from .types import KanbanIdType


class CardType(KanbanModel):
    BoardId = KanbanIdType()
    ColorHex = StringType()
    Id = KanbanIdType()
    IsCardType = BooleanType()
    IsTaskType = BooleanType()
    Name = StringType()
