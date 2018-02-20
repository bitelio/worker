from sys import argv

from worker import Worker


Worker("work" if argv[-1] == "debug" else "live")
