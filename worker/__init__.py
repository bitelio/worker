import time
import raven
import signal
import logging
import leankit

from . import config
from . import database
from . import updater


__author__ = "Guillermo Guirao Aguilar"
__email__ = "info@bitelio.com"
__version__ = "0.0.1"


log = logging.getLogger(__name__)
sentry = raven.Client()


class Worker:
    # TODO: mongo lock -> avoid two workers running
    # server microservice -> refresh, remove, etc.

    def __init__(self, throttle=None):
        self.kill = False
        self.throttle = throttle or config.THROTTLE
        self.version = {board['Id']: board['Version'] for board in
                        database.load.many('boards')}

        signal.signal(signal.SIGINT, self.exit)
        signal.signal(signal.SIGTERM, self.exit)

    def exit(self, signum, frame):
        log.info("Stopping")
        self.kill = True

    def run(self):  # pragma: nocover
        self.refresh()
        while not self.kill:
            try:
                last_update = time.time()
                self.sync()
            except ConnectionError:
                sentry.captureException()
            finally:
                self.sleep(self.throttle + last_update - time.time())
        logging.shutdown()

    def sleep(self, seconds):
        while seconds > 0:
            time.sleep(1)
            seconds -= 1
            if self.kill:
                break

    def sync(self):
        board_ids = database.load.field('settings', 'BoardId', {'Sync': True})
        for board_id in board_ids:
            updater.run(board_id, self.version.get(board_id))

    @staticmethod
    def refresh():
        # TODO: lock file
        log.info('Checking for new boards')
        boards = leankit.get_boards()
        board_ids = database.load.field('settings', 'BoardId')
        new_boards = [board for board in boards if board['Id'] not in board_ids]
        if new_boards:
            database.save.settings(new_boards)

    @staticmethod
    def reset():
        raise NotImplementedError

    @staticmethod
    def remove(board_id):
        raise NotImplementedError


def run():  # pragma: nocover
    log = logging.getLogger(__name__)
    stream_handler = logging.StreamHandler()
    log.setLevel(config.LOGGING)
    log.addHandler(stream_handler)
    log.info("Starting worker")
    worker = Worker(config.THROTTLE)
    worker.run()
