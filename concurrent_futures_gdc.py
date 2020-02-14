# Author: gabri
# File: concurrent_futures_gdc
# Date: 12/07/2019
# Made with PyCharm

# Standard Library
from time import time
from psutil import cpu_count
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Third party modules

# Local application imports


def gcd(pair):
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i


def main():
    numbers = [(1963309, 2265973), (2030677, 3814172),
               (1551645, 2229620), (2039045, 2020802)]

    # Single threaded
    start = time()
    results = list(map(gcd, numbers))
    end = time()
    print('Took % .3f seconds' % (end - start))

    # Using concurrent.futures.ThreadPoolExecutor
    start = time()
    pool1 = ThreadPoolExecutor(max_workers=4)
    results = list(pool1.map(gcd, numbers))
    end = time()
    print('Took % .3f seconds' % (end - start))

    # Using concurrent.futures.ProcessPoolExecutor
    start = time()
    pool2 = ProcessPoolExecutor(max_workers=4)
    results = list(pool2.map(gcd, numbers))
    end = time()
    print('Took % .3f seconds' % (end - start))


if __name__ == "__main__":
    main()
