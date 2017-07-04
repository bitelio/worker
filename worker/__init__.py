#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import signal
import logging

from . import config

__author__ = "Guillermo Guirao Aguilar"
__email__ = "info@bitelio.com"
__version__ = "0.0.1"


log = logging.getLogger(__name__)


class Worker:
    def __init__(self, throttle=60):
        self.kill = False
        self.throttle = throttle
        signal.signal(signal.SIGINT, self.exit)
        signal.signal(signal.SIGTERM, self.exit)

    def exit(self, signum, frame):
        log.info("Stopping worker")
        self.kill = True

    def run(self):  # pragma: nocover
        while True:
            last_update = time.time()
            self.sleep(self.throttle + last_update - time.time())
            if self.kill:
                break

    def sleep(self, seconds):
        while seconds > 0:
            time.sleep(1)
            seconds -= 1
            if self.kill:
                break


def run():  # pragma: nocover
    log.info("Starting worker")
    worker = Worker(config.throttle)
    worker.run()
