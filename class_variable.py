class AddId:
    unique_id = 0

    def __init__(self):
        AddId.sum_id()

    @classmethod
    def sum_id(cls):
        cls.unique_id += 1


a = AddId()
print(a.unique_id)
b = AddId()
print(b.unique_id)
print(a.unique_id)
c = AddId()
print(a.unique_id)
print(b.unique_id)
print(c.unique_id)
