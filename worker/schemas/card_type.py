#!/usr/bin/python
# -*- coding: utf-8 -*-

from schematics.types import StringType
from schematics.types import BooleanType

from . import Model
from .types import KanbanType


class CardType(Model):
    Id = KanbanType()
    Name = StringType()
    ColorHex = StringType()
    IsCardType = BooleanType()
    IsTaskType = BooleanType()
