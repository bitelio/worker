import time
import signal
import logging
import leankit
import traceback

from . import config
from . import database
from . import handler
from . import alerts


__author__ = "Guillermo Guirao Aguilar"
__email__ = "info@bitelio.com"
__version__ = "0.1.0"


log = logging.getLogger(__name__)


class Worker:
    # TODO: mongo lock -> avoid two workers running
    # server microservice -> refresh, remove, etc.

    def __init__(self, throttle=None):
        self.kill = False
        self.alert = alerts.SendGrid()
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
        archive = True
        while not self.kill:
            try:
                last_update = time.time()
                self.sync(archive)
                archive = False
                factor = 1
            except Exception as error:
                log.error(error)
                error_stack = traceback.format_exc()
                print(error_stack)
                self.alert.send(error, error_stack)
                factor += 1
            self.sleep(self.throttle * factor + last_update - time.time())
        logging.shutdown()

    def sleep(self, seconds):
        while seconds > 0:
            time.sleep(1)
            seconds -= 1
            if self.kill:
                break

    def sync(self, archive=False):
        boards = database.load.many('settings', {'Update': True})
        for board in boards:
            # if board['Reindex']:
                # TODO: reset Reindex to false
                # self.reindex(board)
                # pass
            version = self.version.get(board['Id'])
            version = handler.run(board, version, archive)
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
