#!/usr/bin/python
# -*- coding: utf-8 -*-

from .connector import db


def collection(collection, board_id=None, query=None, projection=None):
    query = {**({'BoardId': board_id} if board_id else {}), **(query or {})}
    return list(db[collection].find(query, projection or {'_id': 0}))


def field(collection, field, board_id=None):
    query = {'BoardId': board_id} if board_id else {}
    documents = list(db[collection].find(query, {field: 1}))
    return [document[field] for document in documents]


def dict(key, **kwargs):
    return {doc[key]: doc for doc in collection(**kwargs)}
