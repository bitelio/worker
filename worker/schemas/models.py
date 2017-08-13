#!/usr/bin/python
# -*- coding: utf-8 -*-


from schematics.models import Model
from schematics.exceptions import DataError


class KanbanModel(Model):
    def __init__(self, raw_data, *args, **kwargs):
        try:
            raw_data['BoardId'] = raw_data['Board']['Id']
        except KeyError:
            raise DataError('A reference to the Kanban board is required')
        super().__init__(raw_data, *args, **kwargs)