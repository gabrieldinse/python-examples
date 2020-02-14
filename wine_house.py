class Wine:
    def __init__(self, name, local, year):
        self.name = name
        self.local = local
        self.year = year

    def __str__(self):
        return '{0}, {1} - {2}'.format(self.name, self.local, self.year)


class WineHouse:
    def __init__(self, name, local):
        self.name = name
        self.local = local
        self.wines = []

    def add(self, name, local, year):
        self.wines.append(Wine(name, local, year))

    def pick_by_info(self, name, local, year):
        for wine in self.wines:
            if name == wine.name and local == wine.local and year == wine.year:
                self.wines.remove(wine)
                return wine
        raise RuntimeError('Wine not found')

    def pick_by_index(self, index):
        if index < 0 or index >= len(self.wines):
            raise IndexError('Invalid index')
        return self.wines.pop(index)

    def show(self):
        for wine in self.wines:
            print(wine)


wine_house = WineHouse('dinse', 'blumenau')
wine_house.add('vinho1', 'porto', '1990')
wine_house.add('vinho2', 'chile', '2000')
wine_house.show()
wine = wine_house.pick_by_info('vinho1', 'porto', '1990')
print('')
wine_house.show()
print('')
print(wine)
