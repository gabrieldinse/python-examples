from collections import KeysView, ItemsView, ValuesView

class DictSorted(dict):    
    def __init__(self, *args):
        dict.__init__(self, *args)
        self.ordered_keys = []
    
    def __setitem__(self, key, value):
        '''self[key] = value syntax'''
        if key not in self.ordered_keys:
            self.ordered_keys.append(key)
        super().__setitem__(key, value)
    
    def setdefault(self, key, value):
        if key not in self.ordered_keys:
            self.ordered_keys.append(key)
        return super().setdefault(key, value)

    def keys(self):
        return KeysView(self)

    def values(self):
        return ValuesView(self)

    def items(self):
        return ItemsView(self)

    # Define-se este metodo para quaisquer iteracoes sobre todos os elementos
    # como em 'x in var' ou 'for x in var' que iteram usando __iter__() sobre
    # o dict (var)
    def __iter__(self):
        '''for x in self syntax'''
        return self.ordered_keys.__iter__()


d = DictSorted()
d['b'] = 'b'
d['c'] = 'd'
d['a'] = 'a'
d['1'] = 'c'
d['2'] = 'b'
d2 = dict(d)
a = d['a']
print(d)
print(a)

for key, value in zip(d.keys(), d.values()):
    print(key, value)