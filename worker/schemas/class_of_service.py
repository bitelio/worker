#!/usr/bin/python
# -*- coding: utf-8 -*-

from schematics.types import StringType
from schematics.types import BooleanType

from . import Model
from .types import KanbanType


class ClassOfService(Model):
    Id = KanbanType()
    Title = StringType()
    ColorHex = StringType()
    UseColor = BooleanType()
