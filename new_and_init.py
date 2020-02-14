class Animal(object):
    # Can be omitted, Python will give a default implementation
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)
    
    def __init__(self, name):
        self.name = name
        
a = Animal('Bob')
print(a.name)