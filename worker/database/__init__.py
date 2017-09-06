import yaml
import logging
from os import path

from worker import config
from . import mongo
from . import save
from . import load
from . import update
from . import delete


log = logging.getLogger(__name__)


def init():
    log.info('Checking database')
    names = mongo.db.collection_names()
    for name, options in config.collections.items():
        if name not in names:
            log.info(f'Creating collection: {name}')
            for index in options['indices']:
                unique = index in options['unique']
                mongo.db[name].create_index(index, unique=unique)
