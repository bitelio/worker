import yaml
import logging
from os import path

from .connector import db
from worker import config
from worker import mappings


log = logging.getLogger(__name__)


def init():
    log.info('Checking database')
    names = db.collection_names()
    for name, options in config.collections.items():
        if name not in names:
            log.info(f'Creating collection: {name}')
            for index in options['indices']:
                unique = index in options['unique']
                db[name].create_index(index, unique=unique)


def convert(items):
    def do(value):
        return mappings.get('schema', value)(value).to_native()
    return [do(val) for val in items] if isinstance(items, list) else do(items)
