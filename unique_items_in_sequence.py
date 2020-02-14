# Author: gabri
# File: unique_items_in_sequence
# Date: 29/07/2019
# Made with PyCharm

# Standard Library

# Third party modules

# Local application imports


def unique_sequence(items, key=None):
    seen = set()
    for item in items:
        value = item if key is None else key(item)
        if value not in seen:
            yield value
            seen.add(value)

# If you want to eliminate duplicate lines on files you can use this general
# purpose (unique_sequence) function:
# with open('some_file.txt', 'r') as file:
#     for line in unique_sequence(file):
#         ...


def main():
    # The key parameter is used for not hashable types, like a dict, so it can
    # be converted into a hashable
    a = [{'a': 1, 'b': 2}, {'a': 2, 'b': 1}, {'a': 1, 'b': 2}, {'a': 2, 'b': 1}]
    b = [{'a': 1, 'b': 2}, {'a': 2, 'b': 1}, {'a': 1, 'b': 2}, {'a': 2, 'b': 1}]
    c = [1, 2, 0, 1, 4, 10, 3, 2, 0]

    # In this lambda, the input is 'k'
    print(list(unique_sequence(a, key=lambda k: (k['a'], k['b']))))
    print(list(unique_sequence(a, key=lambda k: k['a'])))
    print(list(unique_sequence(a, key=lambda k: k['b'])))
    print(list(unique_sequence(c)))


if __name__ == "__main__":
    main()
