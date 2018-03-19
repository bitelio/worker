from os import getenv
from sys import stdout
from structlog import configure, stdlib, processors
from logging import getLogger, StreamHandler


log = getLogger("worker")
handler = StreamHandler(stdout)
log.addHandler(handler)

throttle: int = int(getenv("THROTTLE", 60))
timezone: str = getenv("TIMEZONE", "Europe/Berlin")

processors = [stdlib.filter_by_level,
              stdlib.add_log_level,
              stdlib.PositionalArgumentsFormatter(),
              processors.TimeStamper(fmt="iso"),
              processors.StackInfoRenderer(),
              processors.format_exc_info,
              processors.UnicodeDecoder()]

configure(context_class=dict, logger_factory=stdlib.LoggerFactory(),
          wrapper_class=stdlib.BoundLogger, cache_logger_on_first_use=True)
