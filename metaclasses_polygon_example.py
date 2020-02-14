# Author: gabri
# File: metaclasses_polygon_example
# Date: 18/06/2019
# Made with PyCharm

# Standard Library

# Third party modules

# Local application imports


class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        # Don't validate the abstract Polygon class
        if bases != (object,):
            if class_dict['sides'] < 3:
                raise ValueError('Polygons need 3+ sides')
        return type.__new__(meta, name, bases, class_dict)


class Polygon(object, metaclass=ValidatePolygon):
    sides = None  # Specified by subclasses

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180


class Triangle(Polygon):
    sides = 3


class WrongPolygon(Polygon):
    sides = 2


# The program not even start
print('lol')
poly1 = Triangle()
poly2 = WrongPolygon()
