# Author: gabri
# File: metaclass_attribute_anotation
# Date: 10/07/2019
# Made with PyCharm

# Standard Library

# Third party modules

# Local application imports


# Creating a class to represent a database row
class Field:
    def __init__(self, name):
        self.name = None
        self.internal_name = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.internal_name)

    def __set__(self, instance, value):
        setattr(instante, self.internal_name, value)


class Meta(type):
    def __new__(meta, name, bases, class_dict):
        """
        Class containing Field objects. When the class is created, it
        verifies if it have some Field attributes. If it has, change their
        names to the variable name, automatically.
        """
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + value.name
        cls = type.__new__(meta, name, bases, class_dict)
        return cls

class DatabaseRow(metaclass=Meta):
    pass


class Customer(DatabaseRow):
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()


def main():
    pass


if __name__ == "__main__":
    main()
