from . import db
from . import log
from . import save
from . import delete
from . import convert
from .. import mappings


def one(item):
    collection = mappings.get('collection', item)
    db[collection].replace_one({'Id': item['Id']}, convert(item))
    name = mappings.get('name', item)
    log.info(f'{name} updated: {item} ({item.id})')


def card(card):
    one(card)
    delete.many('events', {'CardId': card.id})
    save.many(card.history)
