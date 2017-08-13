#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymongo

from .. import config


client = pymongo.MongoClient(config.MONGODB)
try:
    db = client.get_default_database()
except pymongo.errors.ConfigurationError:
    db = client[config.DATABASE]
