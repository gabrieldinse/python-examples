class C:
    def __init__(self):
        self.__privateMember = 0.0
        self.nonPrivateMember = 1.0

obj = C()
print(obj._C__privateMember)
print(obj.nonPrivateMember)
