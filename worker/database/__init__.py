import yaml
import logging
from os import path

from .connector import db
from .. import mappings


def init():
    log.info('Checking database')
    filename = path.join(path.dirname(__file__), 'collections.yml')
    with open(filename) as models:
        collections = yaml.load(models)
    names = db.collection_names()
    for name, options in collections.items():
        if name not in names:
            log.info('Creating collection: {name}')
            for index in options['indices']:
                unique = index in options['unique']
                db[name].create_index(index, unique=unique)


def convert(items):
    def do(value):
        return mappings.get('schema', value)(value).to_native()
    return [do(val) for val in items] if isinstance(items, list) else do(items)


log = logging.getLogger('worker.database')
elk = logging.getLogger('worker.elk')
# init()
