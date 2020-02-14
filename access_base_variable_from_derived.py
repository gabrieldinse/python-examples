class Base:
    def __init__(self, value):
        self._value = value
        self.string = 'lol'


class Derived(Base):
    def __init__(self, value):
        super().__init__(value)

    def increment_and_print_value(self):
        self._value += 1
        print(self._value)


obj = Derived(10)
obj.increment_and_print_value()
obj.increment_and_print_value()
obj.increment_and_print_value()
