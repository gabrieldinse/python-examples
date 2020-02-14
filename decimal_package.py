# Author: gabri
# File: decimal_package
# Date: 13/07/2019
# Made with PyCharm

# Standard Library
from decimal import Decimal, ROUND_UP
from time import time

# Third party modules

# Local application imports


def main():
    # Case 1
    rate = Decimal('1.453')  # per min
    seconds = Decimal('200')
    cost = rate * seconds / Decimal('60')
    print(cost)
    rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
    print(rounded)

    # Case 2
    rate = Decimal('0.03')
    seconds = Decimal('5')
    cost = rate * seconds / Decimal('60')
    print(cost)
    # Ensures that the cost is rounded to at least 1 cent
    rounded = cost.quantize(Decimal('0.01'), rounding=ROUND_UP)
    print(rounded)


if __name__ == "__main__":
    main()
