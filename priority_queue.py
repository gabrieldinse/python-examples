# Author: gabri
# File: priority_queue
# Date: 28/07/2019
# Made with PyCharm

# Standard Library
import heapq

# Third party modules

# Local application imports


class PriorityQueye:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]  # or [2], in this case


class Item:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Item({!r})'.format(self.name)


def main():
    var = Item('lol')
    print(var)


if __name__ == "__main__":
    main()
