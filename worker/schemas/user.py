#!/usr/bin/python
# -*- coding: utf-8 -*-

from schematics.types import StringType
from schematics.types import BooleanType

from . import Model
from .types import KanbanType


class User(Model):
    Id = KanbanType()
    UserName = StringType()
    FullName = StringType()
    Enabled = BooleanType()
    GravatarLink = StringType()
    Role = StringType(choices=[1, 2, 3, 4])
