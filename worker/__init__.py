import time
import raven
import signal
import logging
import leankit

from . import config
from . import database
from . import handler


__author__ = "Guillermo Guirao Aguilar"
__email__ = "info@bitelio.com"
__version__ = "0.1.0"


log = logging.getLogger(__name__)
sentry = raven.Client()


class Worker:
    # TODO: mongo lock -> avoid two workers running
    # server microservice -> refresh, remove, etc.

    def __init__(self, throttle=None):
        self.kill = False
        self.version = {board['Id']: board['Version'] for board in
                        database.load.many('boards')}
        try:
            self.throttle = int(throttle or config.THROTTLE)
        except ValueError:
            self.throttle = 60

        signal.signal(signal.SIGINT, self.exit)
        signal.signal(signal.SIGTERM, self.exit)

    def exit(self, signum, frame):
        log.info("Stopping")
        self.kill = True

    def run(self):  # pragma: nocover
        log.info("Starting worker")
        self.refresh()
        while not self.kill:
            try:
                last_update = time.time()
                self.sync()
            except Exception as error:
                sentry.captureException()
                if error != ConnectionError or error != IOError:
                    log.fatal(error)
                    raise error
                log.error(error)
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
        boards = database.load.many('settings', {'Update': True})
        for board in boards:
            version = self.version.get(board['Id'])
            version = handler.run(board['Id'], version)
            self.version[board['Id']] = version

    @staticmethod
    def refresh():
        # TODO: lock file
        log.info('Checking for new boards')
        boards = leankit.get_boards()
        board_ids = database.load.field('settings', 'Id')
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
    from logging.config import dictConfig
    dictConfig(config.logging)
    database.init()
    worker = Worker()
    worker.run()
