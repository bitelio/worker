#!/usr/bin/python
# -*- coding: utf-8 -*-

from .connector import db


def document(collection, doc_id, key='Id'):
    db[collection].remove({key: doc_id})
