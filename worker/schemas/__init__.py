#!/usr/bin/python
# -*- coding: utf-8 -*-

from functools import partialmethod
from schematics.models import Model
from schematics.types import BaseType


BaseType.__init__ = partialmethod(BaseType.__init__, required=True)
Model.__init__ = partialmethod(Model.__init__, strict=False, validate=True)
