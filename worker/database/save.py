import logging

from . import mongo
from . import utils
from .. import mappings
from ..schemas.setting import Setting


log = logging.getLogger(__name__)


def one(item):
    collection = mappings.get('collection', item)
    mongo.db[collection].insert_one(utils.convert(item))
    name = mappings.get('name', item)
    log.info(f'{name} created: {item} ({item.id})')


def many(items):
    items = list(items)
    collection = mappings.get('collection', items[0])
    mongo.db[collection].insert_many(utils.convert(items))
    name = collection.replace('_', ' ')
    log.info(f'{len(items)} {name} created')


def settings(boards):
    data = [Setting(board).to_native() for board in boards]
    mongo.db.settings.insert(data)
    log.info(f'{len(boards)} new boards found')


def card(card):
    one(card)
    many(card.history)
