#!/usr/bin/python
# -*- coding: utf-8 -*-

from schematics.types import StringType
from schematics.types import BooleanType

from .models import KanbanModel
from .types import KanbanIdType


class User(KanbanModel):
    BoardId = KanbanIdType()
    Enabled = BooleanType()
    FullName = StringType()
    GravatarLink = StringType()
    Id = KanbanIdType()
    Role = StringType(choices=[1, 2, 3, 4])
    UserName = StringType()
