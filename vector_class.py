# Author: gabri
# File: vector_class
# Date: 10/02/2020
# Made with PyCharm

# Standard Library
from math import sqrt
from itertools import zip_longest

# Third party modules

# Local application imports


class Vector:
    def __init__(self, *args, default=0.0, dtype=float):
        self.default = default
        self.dtype = dtype
        if args:
            self._values = []
            for val in args:
                self._values.append(self.dtype(val))
            self._values = tuple(self._values)
        else:
            self._values = (0.0, 0.0)

    def __repr__(self):
        return f'Vector{self._values}'

    def __eq__(self, other):
        return self._values == other

    def __lt__(self, other):
        return abs(self) < abs(other)

    def __len__(self):
        return len(self._values)

    def __iter__(self):
        return self._values.__iter__()
    
    def __getitem__(self, item):
        if item >= len(self):
            return self.default
        else:
            return self._values[item]

    def __abs__(self):
        return sqrt(self.inner(self))

    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        return Vector(*tuple(val1 + val2 for val1, val2 in zip_longest(
            self, other, fillvalue=self.default)))

    def __sub__(self, other):
        return Vector(*tuple(val1 - val2 for val1, val2 in zip_longest(
            self, other, fillvalue=self.default)))

    def __mul__(self, other):
        if type(self) == type(other):
            return self.inner(other)
        elif type(other) == type(1) or type(other) == type(1.0):
            return Vector(*tuple(val * other for val in self))

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if type(other) == type(1) or type(other) == type(1.0):
            return Vector(*tuple(val / other for val in self))

    def norm(self):
        return abs(self)

    def inner(self, other):
        return sum(val1 * val2 for val1, val2 in zip_longest(
            self, other, fillvalue=self.default))

    def cross(self, other):
        if len(self) <= 3 and len(other) <= 3:
            a = [self[i] if i < len(self) else self.default for i in range(3)]
            b = [other[i] if i < len(other) else other.default for i in range(3)]
            return Vector(a[1] * b[2] - a[2] * b[1],
                          a[2] * b[0] - a[0] * b[2],
                          a[0] * b[1] - a[1] * b[0])

    def normalize(self):
        return Vector(*tuple(val / abs(self) for val in self))


def main():
    pass


if __name__ == "__main__":
    main()
