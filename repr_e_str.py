class Class:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return '{0}({1})'.format(type(self).__name__, self.value)


c = Class(100.01)
print(repr(c))
print(c)
b = eval(repr(c))
print(b)
