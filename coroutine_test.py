def coroutine():
    print('pre first yield')
    var = yield
    print('pos first yield and pre while')
    while True:
        print(var)
        print('pre second yield and pos while')
        var = yield [4, 5, 6]
        print('pos second yield and pos while')
        