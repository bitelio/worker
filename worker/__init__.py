__author__ = "Guillermo Guirao Aguilar"
__email__ = "info@bitelio.com"
__version__ = "0.1.0"


import time
import signal
import leankit
import importlib
import schematics

from . import env
from .utils import lock
from .board import Updater
from .schemas.board import Board


class Worker:
    def __init__(self, environment: str) -> None:
        importlib.import_module(f"worker.env.{environment}")
        self.kill = False
        self.boards: dict = {}
        signal.signal(signal.SIGINT, self.exit)
        signal.signal(signal.SIGTERM, self.exit)
        with lock("worker", blocking_timeout=1):
            env.log.info(f"Starting worker in {environment} mode")
            self.run()

    def exit(self, signum, frame):
        env.log.info("Stopping")
        self.kill = True

    def run(self):  # pragma: nocover
        self.refresh()
        backoff = 1
        while not self.kill:
            last_update = time.time()
            try:
                self.sync()
                backoff = 1
            except Exception as error:
                env.log.error(error, exc_info=True)
                backoff *= 2
            self.sleep(env.throttle * backoff + last_update - time.time())
            self.jobs()

    def sleep(self, seconds):
        while seconds > 0:
            time.sleep(1)
            seconds -= 1
            if self.kill:
                break

    def sync(self):
        boards = env.cache.get("worker:boards")
        if boards:
            try:
                board_ids = [int(board_id) for board_id in boards.split()]
            except ValueError:
                env.log.error("Invalid sync ids format")
            else:
                for board_id in board_ids:
                    with lock(f'write:{board_id}'):
                        if board_id in self.boards:
                            self.boards[board_id].update()
                        else:
                            try:
                                self.boards[board_id] = Updater(board_id)
                            except schematics.DataError:
                                env.log.warning(f"Removing board {board_id}")
                                boards.remove(board_id)
                                env.cache.set("worker:boards", boards)
                                return
                    env.cache.set(f"worker:{board_id}", int(time.time()))

    def jobs(self):
        job = env.cache.lpop("worker:jobs")
        while job:
            try:
                action, board_id = job.split(":")
                getattr(self.boards[board_id], action)()
            except (ValueError, AttributeError, KeyError, TypeError) as error:
                env.log.error(f"Invalid job: {job} - {error}")
            finally:
                job = env.cache.lpop("worker:jobs")

    @staticmethod
    def refresh():
        env.log.info('Refreshing boards')
        boards = {board["Id"]: board for board in leankit.get_boards()}
        board_ids = [board["Id"] for board in env.db.boards.find()]
        new_boards = [Board(board).populate() for board in boards.values()
                      if board["Id"] not in board_ids]
        if new_boards:
            env.db.boards.insert_many(new_boards)
            env.log.info(f"{len(new_boards)} new boards available")

        old_boards = [board_id for board_id in board_ids
                      if board_id not in boards]
        if old_boards:
            env.db.boards.delete_many({"Id": {"$in": old_boards}})
            env.log.info(f"{len(new_boards)} boards removed")
