class Date:
    def __init__(self, month=0, day=0, year=0):
        self.month = month
        self.day = day
        self.year = year

    def __str__(self):
        return '%s-%s-%s' % (self.month, self.day, self.year)

    @classmethod
    def from_string(cls, date):
        month, day, year = map(int, date.split('-'))
        return cls(month, day, year)


date1 = Date(10, 10, 2010)
date2 = Date.from_string('02-04-1997')
print(date1)
print(date2)
