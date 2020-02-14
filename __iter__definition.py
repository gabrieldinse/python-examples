class StrangeList:
    def __init__(self, items):
        self.items = items
        
    def __iter__(self):
        yield 5
        yield 10
        for elem in self.items:
            yield elem
            
items = [1, 2, 3, 4, 5, 6, 7, 8, 9]
var = StrangeList(items)
it = iter(var)

print('#1')
for x in it:
    print(x)

print('\n#2')    
for x in it:
    print(x)

# Necessario renover um iterator para utliza-lo novamente ou usar
# 'elem in var' (itera sobre var)
print('\n#3')
for x in var:
    print(x)

print('\n#4')
for x in var:
    print(x)