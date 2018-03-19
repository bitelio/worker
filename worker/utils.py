from contextlib import contextmanager

from . import env


@contextmanager
def lock(name: str, *args, **kwargs):
    lock = env.cache.lock(name, *args, **kwargs)
    if lock.acquire():
        try:
            yield
        finally:
            lock.release()
    else:
        print(f"Couldn't acquire lock '{name}'")
        exit(1)
