# Author: Gabriel Dinse
# File: shared_value_between_objects
# Date: 23/05/2019
# Made with PyCharm

# Standard Library

# Third party modules

# Local application imports


class Shared:
    def __init__(self):
        self.value = 0


class Class:
    def __init__(self, shared):
        self._shared = shared

    @property
    def value(self):
        return self._shared.value

    @value.setter
    def value(self, value):
        self._shared.value = value


def main():
    shared = Shared()
    obj1 = Class(shared)
    obj2 = Class(shared)
    print(obj1.value)
    print(obj2.value)
    obj1.value = -9999
    print(obj1.value)
    print(obj2.value)
    obj1.value = 100
    print(obj1.value)
    print(obj2.value)


if __name__ == "__main__":
    main()
