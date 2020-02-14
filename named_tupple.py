from collections import namedtuple

# eh como criar uma nova classe 
Point = namedtuple('Point', ['x', 'y'])
p = Point(1.23, -34.4123)
print(p)