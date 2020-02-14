def process_value_coroutine():
    """ This coroutine process and return the value * 2 on send """
    print('Initializing coroutine')
    value = yield
    while True:
        value = yield value * 2