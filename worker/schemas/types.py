#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime, date
from schematics.types import IntType
from schematics.types import DateType
from schematics.exceptions import ValidationError


class KanbanIdType(IntType):
    MESSAGES = {'id_length': "Kanban ids must have 9 digits"}

    def to_native(self, value, *args, **kwargs):
        value = super().to_native(value, *args, **kwargs)

        if len(str(value)) != 9:
            raise ValidationError(self.messages['id_length'])
        return value


class MongoDateType(DateType):
    SERIALIZED_FORMAT = '%Y-%m-%dT%H:%M:%S'

    def to_native(self, value, *args, **kwargs):
        if isinstance(value, date):
            return datetime.combine(value, datetime.min.time())
        else:
            value = super().to_native(value, *args, **kwargs)
