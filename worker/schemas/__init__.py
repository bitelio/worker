#!/usr/bin/python
# -*- coding: utf-8 -*-

from functools import partialmethod
from schematics.models import Model as OriginalModel
from schematics.exceptions import ConversionError
from schematics.undefined import Undefined
from schematics.types import BaseType


class Model(OriginalModel):
    def __init__(self, raw_data, **kwargs):
        kwargs['strict'] = False
        if 'Board' in raw_data:
            raw_data['BoardId'] = raw_data['Board']['Id']
        super().__init__(raw_data, **kwargs)


BaseType.__init__ = partialmethod(BaseType.__init__, required=True)
