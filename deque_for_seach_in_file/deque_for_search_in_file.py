# Author: gabri
# File: deque_for_search_in_file
# Date: 27/07/2019
# Made with PyCharm

# Standard Library
from collections import deque

# Third party modules

# Local application imports


def search(lines, pattern, history=5):
    previous_lines = deque(maxlen=history)
    for line in lines:
        if pattern in line:
            yield line, previous_lines
        previous_lines.append(line)


# Example use on a file
if __name__ == '__main__':
    with open('file.txt') as f:
        lines = search(f, 'python', 5)
        print(type(lines))
        for line, prevlines in lines:
            for pline in prevlines:
                print(pline, end='')
            print(line, end='')
            print('-' * 20)  # 20 times the '-' character
