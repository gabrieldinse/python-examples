# Author: gabri
# File: cannibals_dinner
# Date: 31/08/2019
# Made with PyCharm

# Standard Library
import threading
import time
import random
import enum

# Third party modules

# Local application imports


class Cannibal(threading.Thread):
    def __init__(self, cannibal_id, lock=None, portions_semaphore=None,
                 cooker_lock=None):
        super().__init__()
        self.id = cannibal_id
        self.can_run = False
        self.lock = lock
        self.portions_semaphore = portions_semaphore
        self.cooker_lock = cooker_lock

    def serve_yourself(self):
        self.lock.acquire()
        if self.portions_semaphore.acquire(False):
            print("Cannibal {} got a portion".format(self.id))
            self.lock.release()
            time.sleep(random.uniform(1.0, 4.0))
        else:
            self.wake_up_cooker()

    def wake_up_cooker(self):
        print("Cooker was woken by cannibal {}".format(self.id))
        self.cooker_lock.release()

    def start(self):
        self.can_run = True
        super().start()

    def run(self):
        while self.can_run:
            self.serve_yourself()

    def stop(self):
        self.can_run = False


class Cooker(threading.Thread):
    def __init__(self, number_of_portions, cannibals_lock=None):
        super().__init__()
        self.number_of_portions = number_of_portions
        self.portions_semaphore = threading.Semaphore(0)
        self.lock = threading.Lock()
        self.lock.acquire()
        self.cannibals_lock = cannibals_lock
        self.can_run = False

    def prepare_dinner(self):
        self.lock.acquire()
        print("Cooker started preparing the dinner")
        for i in range(self.number_of_portions):
            time.sleep(random.uniform(0.0, 1.0))
            print("Cooker prepared one portion")
            self.portions_semaphore.release()
        print("Cooker went to sleep")
        self.cannibals_lock.release()

    def start(self):
        self.can_run = True
        super().start()

    def run(self):
        while self.can_run:
            self.prepare_dinner()

    def stop(self):
        self.can_run = False


def cannibals_dinner(number_of_cannibals, number_of_portions):
    cannibals_lock = threading.Lock()
    cooker = Cooker(number_of_portions, cannibals_lock=cannibals_lock)
    cannibals = []
    for i in range(number_of_cannibals):
        cannibals.append(
            Cannibal(i, lock=cannibals_lock,
                     portions_semaphore=cooker.portions_semaphore,
                     cooker_lock=cooker.lock))

    cooker.start()
    for cannibal in cannibals:
        cannibal.start()

    return cooker, cannibals


def main():
    number_of_cannibals = int(input('Enter the number of cannibals: '))
    number_of_portions = int(input('Enter the number of portions: '))
    cooker, cannibals = cannibals_dinner(number_of_cannibals,
                                         number_of_portions)
    _ = input('Press ENTER to stop . . .\n')

    print('Time to finish the dinner!')
    cooker.stop()
    for cannibal in cannibals:
        cannibal.stop()


if __name__ == "__main__":
    main()
