def func(numA, numB):
    return numA * numB

def printAll(*args):
    print(args)


# so funciona com 2 argumentos
def operation(*args):
    return func(*args)
    
printAll('a', 2.312, ['lol', 2], 5, 'kkkk')
print(operation(2, 2))