# Author: Gabriel Dinse
# File: multiprocessing_example_pool
# Date: 07/06/2019
# Made with PyCharm

# Standard Library
import random
from multiprocessing.pool import Pool

# Third party modules

# Local application imports


def prime_factor(value):
    factors = []
    for divisor in range(2, value - 1):
        quotient, remainder = divmod(value, divisor)
        if not remainder:
            factors.extend(prime_factor(divisor))
            factors.extend(prime_factor(quotient))
            break
        else:
            factors = [value]
    return factors


def main():
    pool = Pool()
    to_factor = [random.randint(100000, 50000000) for i in range(20)]
    results = pool.map(prime_factor, to_factor)
    for value, factors in zip(to_factor, results):
        print("The factors of {} are {}".format(value, factors))


if __name__ == "__main__":
    main()
