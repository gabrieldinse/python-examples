def variableArgumentsSum(a, b, *args):
    result = a + b
    print(type(args))
    for num in args:
        result += num
    return result


# python 3
def optionalArgumentsPrice1(value, tax_percentage=0, discount=0):
    value += value * (tax_percentage / 100) - discount
    return value


# python 2
def optionalArgumentsPrice2(value, **kwargs):
    print(type(kwargs))
    tax_percentage = kwargs.get('tax_percentage')
    discount = kwargs.get('discount')
    if tax_percentage:
        value += value * (tax_percentage / 100)
    if discount:
        value -= discount
    return value


print(variableArgumentsSum(1.0, 2))
print(variableArgumentsSum(1.0, 2, 3, 4, 6.7))
print(optionalArgumentsPrice1(100.0))
print(optionalArgumentsPrice1(100.0, discount=50))
print(optionalArgumentsPrice1(100.0, tax_percentage=25.5))
print(optionalArgumentsPrice1(100.0, discount=20, tax_percentage=25.5))
print(optionalArgumentsPrice2(100.0))
print(optionalArgumentsPrice2(100.0, discount=50))
print(optionalArgumentsPrice2(100.0, tax_percentage=25.5))
print(optionalArgumentsPrice2(100.0, discount=20, tax_percentage=25.5))
