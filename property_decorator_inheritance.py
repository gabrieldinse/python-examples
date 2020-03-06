# Author: gabri
# File: property_decorator_inheritance
# Date: 06/09/2019
# Made with PyCharm

# Standard Library

# Third party modules

# Local application imports


class A:
    def __init__(self):
        self._var = 1

    @property
    def var(self):
        return self._var

    @var.setter
    def var(self, value):
        self._var = value


class B(A):
    pass

def main():
    b = B()
    print(b.var)
    b.var = 10
    print(b.var)


if __name__ == "__main__":
    main()
