import cProfile
import functools
import time
import pstats
from io import StringIO


def profile_deco(func):
    profiler = cProfile.Profile()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return profiler.runcall(func, *args, **kwargs)

    def print_stat():
        stream = StringIO()
        stats = pstats.Stats(profiler, stream=stream)
        stats.strip_dirs()
        stats.sort_stats("cumulative")
        stats.print_stats()
        print(stream.getvalue())

    wrapper.print_stat = print_stat
    return wrapper


@profile_deco
def add(arg1, arg2):
    time.sleep((arg1 + arg2) / 1_000_000)
    return arg1 + arg2


@profile_deco
def sub(arg1, arg2):
    time.sleep(abs(arg1 - arg2) / 1_000_000)
    return arg1 - arg2


if __name__ == "__main__":
    for i in range(1000):
        add(i, i + 1)

    for i in range(500):
        sub((3 * i) % 5, (5 * i) % 7)

    add.print_stat()
    sub.print_stat()
