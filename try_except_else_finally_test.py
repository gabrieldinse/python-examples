import random
some_exceptions = [ValueError, TypeError, IndexError, None]


def exception_handling():
    """ Funcao para testar a funcionalidade de exception handling com
    exceptions aleatorias.
    Utiliza: try, except, else, finally.
    """
    try:
        choice = random.choice(some_exceptions)
        print("raising {}".format(choice))
        if choice:
            raise choice("An error")
    except ValueError:
        print("Caught a ValueError")
    except TypeError:
        print("Caught a TypeError")
    except Exception as e:
        print("Caught some other error: %s" % (e.__class__.__name__))
    else:
        print("This code called if there is no exception")
    finally:
        print("This cleanup code is always called")
