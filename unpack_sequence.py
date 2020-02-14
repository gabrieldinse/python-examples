# Author: gabri
# File: unpack_sequence
# Date: 24/07/2019
# Made with PyCharm

# Standard Library

# Third party modules

# Local application imports


def main():
    # Star unpacking
    some_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    value1, *middle, value2 = some_list
    print(value1, value2)  # only the first and last values
    print(middle)


if __name__ == "__main__":
    main()
