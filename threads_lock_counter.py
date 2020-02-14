# Author: gabri
# File: threads_lock_counter
# Date: 11/07/2019
# Made with PyCharm

# Standard Library
from threading import Thread, Lock

# Third party modules

# Local application imports


class LockingCounter:
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset


class NoLockCounter:
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset


def worker(counter, how_many):
    for _ in range(how_many):
        counter.increment(1)


def run_threads(worker_func, how_many, counter, num_threads):
    threads = []
    for _ in range(num_threads):
        args = (counter, how_many)
        thread = Thread(target=worker_func, args=args)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def main():
    # The operation counter.increment(offset) takes three separate operations to
    # be evaluated:
    # #1) value = getattr(counter, 'count')
    # #2) result = value + offset
    # #3) setattr(counter, 'count', result)

    # If you try to run this with threads, you may have problemas with data
    # racing. To solve this, it necessary to use a threading.Lock(), to
    # syncronize some parts of the code where multiple threads try access and
    # mofidy the same data.

    print('Locking Counter')
    how_many = 100000
    num_threads = 5
    counter = LockingCounter()
    run_threads(worker, how_many, counter, num_threads)
    print('Expected: {}'.format(how_many * num_threads))
    print('Found: {}\n'.format(counter.count))

    print('Counter Without Lock')
    how_many = 100000
    num_threads = 5
    counter = NoLockCounter()
    run_threads(worker, how_many, counter, num_threads)
    print('Expected: {}'.format(how_many * num_threads))
    print('Found: {}\n'.format(counter.count))


if __name__ == "__main__":
    main()
