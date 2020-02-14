# Author: gabri
# File: jantar_do_filosofos
# Date: 30/08/2019
# Made with PyCharm

# Standard Library
import threading
from enum import Enum
import time
import random

# Third party modules

# Local application imports


class PhilsopherState(Enum):
    Thinking = "Thinking"
    Eating = "Eating"
    Hungry = "Hungry"


class Philosopher(threading.Thread):
    output_lock = threading.Lock()

    def __init__(self, philosopher_id, left_fork=None, right_fork=None):
        super().__init__()
        self.id = philosopher_id
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.can_run = False
        self.state = PhilsopherState.Thinking  # initialize thinking

    def think(self):
        with self.output_lock:
            print('Philosopher {} is thinking'.format(self.id))
        time.sleep(random.randint(1, 10))
        self.state = PhilsopherState.Hungry

    def starve(self):
        with self.output_lock:
            print('Philosopher {} is hungry'.format(self.id))
        if self.left_fork.acquire(False):
            if self.right_fork.acquire(False):
                self.state = PhilsopherState.Eating
            else:
                self.left_fork.release()
                time.sleep(random.randint(1, 10))
        else:
            time.sleep(random.randint(1, 10))

    def eat(self):
        with self.output_lock:
            print('Philosopher {} is eating'.format(self.id))
        time.sleep(random.randint(1, 10))
        with self.output_lock:
            print('Philosopher {} stopped eating'.format(self.id))
        self.state = PhilsopherState.Thinking
        self.left_fork.release()
        self.right_fork.release()

    def run(self):
        with self.output_lock:
            print('Philosopher {} running'.format(self.id))
        while self.can_run:
            if self.state == PhilsopherState.Thinking:
                self.think()
            elif self.state == PhilsopherState.Hungry:
                self.starve()
            elif self.state == PhilsopherState.Eating:
                self.eat()

    def start(self):
        self.can_run = True
        super().start()

    def stop(self):
        self.can_run = False


def philosophers_dinner(num_philosophers):
    forks = [threading.Lock() for _ in range(num_philosophers)]
    philosophers = []
    for i in range(num_philosophers - 1):
        philosophers.append(Philosopher(i + 1, forks[i], forks[i + 1]))
    philosophers.append(
        Philosopher(num_philosophers, forks[num_philosophers - 1], forks[0]))

    for philosopher in philosophers:
        philosopher.start()

    return philosophers


def main():
    num_philosophers = int(input('Enter the number of philosophers: '))
    philosophers = philosophers_dinner(num_philosophers)
    _ = input('Press ENTER to stop . . .\n')

    print('Time to finish the dinner!')
    for philosopher in philosophers:
        philosopher.stop()


if __name__ == "__main__":
    main()
