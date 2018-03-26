from os import getenv, path
from sys import stdout
from yaml import safe_load
from logging import getLogger, StreamHandler
from structlog import configure, stdlib, processors, get_logger


def setup(db):
    log = get_logger("worker")
    filename = path.join(path.dirname(__file__), "collections.yml")
    with open(filename) as data:
        collections = safe_load(data)
    log.info("Checking database")
    names = db.collection_names()
    for name, options in collections.items():
        if name not in names:
            log.info("Setting up indices", collection=name)
            for index in options['indices']:
                unique = index in options['unique']
                db[name].create_index(index, unique=unique)


log = getLogger("worker")
handler = StreamHandler(stdout)
log.addHandler(handler)

throttle: int = int(getenv("THROTTLE", 60))
timezone: str = getenv("TIMEZONE", "Europe/Berlin")

processors = [stdlib.filter_by_level,
              stdlib.add_log_level,
              stdlib.PositionalArgumentsFormatter(),
              processors.StackInfoRenderer(),
              processors.format_exc_info,
              processors.UnicodeDecoder()]

configure(context_class=dict, logger_factory=stdlib.LoggerFactory(),
          wrapper_class=stdlib.BoundLogger, cache_logger_on_first_use=True)
