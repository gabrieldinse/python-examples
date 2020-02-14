# Author: Gabriel Dinse
# File: iterator__iter__next
# Date: 12/06/2019
# Made with PyCharm

# Standard Library

# Third party modules

# Local application imports


class Range:
    def __init__(self, max_index):
        self.max_index = max_index

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n >= self.max_index:
            raise StopIteration

        self.n += 1
        return self.n - 1


def main():
    for i in Range(10):
        print(i)


if __name__ == "__main__":
    main()
