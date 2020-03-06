# Author: gabri
# File: property
# Date: 06/03/2020
# Made with PyCharm

# Standard Library

# Third party modules

# Local application imports


class A:
    def __init__(self):
        self._attribute = "Default value"

    @property
    def attribute(self):
        return self._attribute

    @attribute.setter
    def attribute(self, value):
        self._attribute = value


class B(A):
    pass


def main():
    pass


if __name__ == "__main__":
    main()
