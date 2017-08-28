from . import db
from . import log
from . import save
from . import delete
from . import convert
from .. import mappings
from .. import schemas


def one(item):
    collection = mappings.get('collection', item)
    db[collection].replace_one(convert(item))
    name = mappings.get('name', item)
    log.info(f'{name} updated: {item} ({item.id})')


def many(items, query):
    delete.many('events', query)
    save.many(items)


def settings(boards):
    if boards:
        data = [schemas.setting(board).to_native() for board in boards]
        db.settings.insert(data)
        log.info(f'{len(items)} new boards found')


def card(card):
    one(card)
    many(card.history, {'CardId': card.id})
