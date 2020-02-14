import time
from functools import wraps


def exec_time(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        function_return = function(*args, **kwargs)
        print('{0} evaluation time: {1}'.format(function.__name__,
                                                time.time() - start_time))
        return function_return
    return wrapper


@exec_time
def some_function(value):
    print(value)


some_function(1)
print('\n')
some_function([i for i in range(10000)])
print(some_function)
