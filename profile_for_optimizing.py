# Author: gabri
# File: profile_for_optimizing
# Date: 15/07/2019
# Made with PyCharm

# Standard Library
from cProfile import Profile
from pstats import Stats
from random import randint
from bisect import bisect_left

# Third party modules

# Local application imports


def insertion_sort(data):
    result = []
    for value in data:
        insert_value(result, value)
    return result


def insert_value(array, value):
    for i, existing in enumerate(array):
        if existing > value:
            array.insert(i, value)
            return
    array.append(value)


def better_insert(array, value):
    # 'bisect_left' returns the correct position where the value can be
    # inserted, maintaining the sorting order. It has logaritmic complexity.
    i = bisect_left(array, value)
    array.insert(i, value)


def better_insertion_sort(data):
    result = []
    for value in data:
        better_insert(result, value)
    return result


def main():
    max_size = 10 ** 4
    data = [randint(0, max_size) for _ in range(max_size)]
    test = lambda: insertion_sort(data)
    test2 = lambda: better_insertion_sort(data)

    profiler = Profile()
    profiler.runcall(test)
    stats = Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats('cumulative')
    stats.print_stats()

    profiler2 = Profile()
    profiler2.runcall(test2)
    stats = Stats(profiler2)
    stats.strip_dirs()
    stats.sort_stats('cumulative')
    stats.print_stats()


if __name__ == "__main__":
    main()
