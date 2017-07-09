#!/usr/bin/python
# -*- coding: utf-8 -*-

from schematics.models import Model as OriginalModel
from schematics.types import BaseType


class Model(OriginalModel):
    def __init__(self, raw_data, **kwargs):
        kwargs['strict'] = False
        if 'Board' in raw_data:
            raw_data['BoardId'] = raw_data['Board']['Id']
        super().__init__(raw_data, **kwargs)


def patch(self, **kwargs):
    if 'required' not in kwargs:
        kwargs['required'] = True
    init(self, **kwargs)


init = BaseType.__init__
BaseType.__init__ = patch
