#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import raven
import signal
import logging
import leankit

from . import config
from . import database
# from . import compare

__author__ = "Guillermo Guirao Aguilar"
__email__ = "info@bitelio.com"
__version__ = "0.0.1"


log = logging.getLogger(__name__)
sentry = raven.Client()


class Worker:
    def __init__(self, throttle=None):
        self.kill = False
        self.throttle = throttle or config.THROTTLE
        self.version = {board['Id']: board['Version'] for board in
                        database.load.collection('boards')}

        signal.signal(signal.SIGINT, self.exit)
        signal.signal(signal.SIGTERM, self.exit)

    def exit(self, signum, frame):
        log.info("Stopping")
        self.kill = True

    def run(self):  # pragma: nocover
        while not self.kill:
            try:
                last_update = time.time()
                self.sync()
            except ConnectionError:
                sentry.captureException()
            finally:
                self.sleep(self.throttle + last_update - time.time())

    def sleep(self, seconds):
        while seconds > 0:
            time.sleep(1)
            seconds -= 1
            if self.kill:
                break

    def populate(self):
        """ Populates the settings collections with all available boards """
        log.info('Populating database')
        boards = leankit.get_boards()
        ids = database.load.field('settings', 'Id')
        new = [board for board in boards if board.id not in ids]
        if new:
            database.save.collection('settings', new)

    def sync(self):
        settings = database.load.settings(query={'Sync': True})
        for board in settings:
            self.populate()
            self.sync()
        else:
            for board in settings:
                self.check(board)

    def check(self, board_id):
        version = self.version.get(board_id, 0)
        board = leankit.get_newer_if_exists(board_id, version, config.timezone)
        if board:
            log.info('Updating {0} ({0.id}) to v{0.version}'.format(board))
            if version == 0:
                # Deactivate logging
                board.get_archive()
            self.update(board)

    def update(self, board):
        # compare.lanes(board)
        # lanes & others
        # cards
        # history
        pass

    def archive(self, board):
        """ Check for new cards in archive """
        if board.top_level_archive_lane_id not in board.lanes:
            board.get_archive()


def run():  # pragma: nocover
    stream_handler = logging.StreamHandler()
    log.setLevel(config.LOGGING)
    log.addHandler(stream_handler)
    log.info("Starting worker")
    worker = Worker(config.throttle)
    worker.run()
