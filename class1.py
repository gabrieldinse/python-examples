class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class Rectangle:
    """ Representa um retangulo no ponto corner """

    def __init__(self, width, height, corner=Point()):
        self.width = width
        self.height = height
        self.corner = corner

    def __str__(self):
        return '%gx%g at (%g,%g)' % (self.width, self.height, self.corner.x,
                                     self.corner.y)

    def __lt__(self, other):
        return self.area() < other.area()

    def __eq__(self, other):
        return self.area() == other.area()

    def area(self):
        return self.width * self.height


class C(list):
    pass


rec = Rectangle(10.2, 6.67, Point(3.20, -1.45))
var = C()
var.append('a')
print(var)
print(rec)
print(rec.area())
print(rec == Rectangle(10.2, 6.67))

