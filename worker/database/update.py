import logging

from . import mongo
from . import save
from . import delete
from . import utils
from .. import mappings


log = logging.getLogger(__name__)


def one(item):
    collection = mappings.get('collection', item)
    mongo.db[collection].replace_one({'Id': item['Id']}, utils.convert(item))
    name = mappings.get('name', item)
    log.info(f'{name} updated: {item} ({item.id})')


def card(card, events=None):
    one(card)
    save.many(events or card.history)
