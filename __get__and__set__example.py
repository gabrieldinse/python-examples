# Author: gabri
# File: __get__and__set__example
# Date: 17/06/2019
# Made with PyCharm

# Standard Library

# Third party modules

# Local application imports


class NonNegative:
    def __get__(self, instance, owner):
        print('__get__ called with {} '
              'instance for class {}'.format(instance, owner))
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        print('__set__ called with {} '
              'instance for value {}'.format(instance, value))
        if value < 0:
            raise ValueError('Cannot be negative.')
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        print('__set_name__ called with {} '
              'class for name {}'.format(owner, name))
        self.name = name


class Order:
    price = NonNegative()
    quantity = NonNegative()

    def __init__(self, name, price, quantity):
        self._name = name
        self.price = price
        self.quantity = quantity

    def total(self):
        return self.price * self.quantity


print('')
apple_order = Order('apple', 1, 10)
apple_order.total()
# 10
apple_order.price = 10
# ValueError: Cannot be negative
apple_order.quantity = -10
# ValueError: Cannot be negative
print('')
another_order = Order('lol', 10, 100)
print(apple_order.total())
print('')
print(another_order.total())
print('')
another_order2 = Order('apple', 20, 30)
print(apple_order.total())
print(another_order2.total())