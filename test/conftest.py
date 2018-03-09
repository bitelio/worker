from pytest import fixture

from worker.env import test


@fixture(scope="session", autouse=True)
def seed():
    test.cache.set("boards", "100000000")
