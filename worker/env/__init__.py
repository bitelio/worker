from os import getenv
from functools import partial
from logging import getLogger, Formatter, StreamHandler


log = getLogger("worker")
formatter = Formatter("%(asctime)s │ %(levelname)9s │ %(board)9s │ %(message)s")
handler = StreamHandler()
handler.setFormatter(formatter)
log.addHandler(handler)
throttle: int = getenv("THROTTLE", 60)
log._log = partial(log._log, extra={"board": ""})
