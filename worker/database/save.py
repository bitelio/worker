#!/usr/bin/python
# -*- coding: utf-8 -*-

from .. import log
from .. import mappings

from .connector import db


def document(collection, item):
    collection = mappings.get('collection', item)
    schema = mappings.get('schema', item)
    data = schema(item).serialize()
    db[collection].insert(data)
    name = mappings.get('name', item)
    log.info('{0} created: {1} ({1.id})'.format(name, item))
