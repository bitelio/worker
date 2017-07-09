#!/usr/bin/python
# -*- coding: utf-8 -*-

from schematics.types import IntType
from schematics.exceptions import ValidationError


class KanbanType(IntType):
    MESSAGES = {'id_length': "Kanban ids must have 9 digits"}

    def to_native(self, value, context):
        value = super().to_native(value, context)

        if len(str(value)) != 9:
            raise ValidationError(self.messages['id_length'])
        return value
