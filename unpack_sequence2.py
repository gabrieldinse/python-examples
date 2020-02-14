# Author: gabri
# File: unpack_sequence2
# Date: 27/07/2019
# Made with PyCharm

# Standard Library

# Third party modules

# Local application imports

records = [('foo', 1, 2), ('bar', 'hello'), ('foo', 3, 4)]


def do_foo(x, y):
    print('foo', x, y)


def do_bar(s):
    print('bar', s)


def main():
    for tag, *args in records:
        print(type(args))
        # The '*' syntax turns the sequence into a argument list
        if tag == 'foo':
            do_foo(*args)
        elif tag == 'bar':
            do_bar(*args)


if __name__ == "__main__":
    main()
