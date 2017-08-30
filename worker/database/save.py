from . import db
from . import log
from . import convert
from .. import mappings
from ..schemas.setting import Setting


def one(item):
    collection = mappings.get('collection', item)
    db[collection].insert_one(convert(item))
    name = mappings.get('name', item)
    log.info(f'{name} created: {item} ({item.id})')


def many(items):
    items = list(items)
    collection = mappings.get('collection', items[0])
    db[collection].insert_many(convert(items))
    name = mappings.get('name', items[0])
    name = collection.replace('_', ' ')
    # log.info(f'{len(items)} {name} created')


def settings(boards):
    data = [Setting(board).to_native() for board in boards]
    db.settings.insert(data)
    log.info(f'{len(boards)} new boards found')


def card(card):
    one(card)
    many(card.history)
