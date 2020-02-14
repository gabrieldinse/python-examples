import pickle

class Foo(object):
    def __init__(self, val=2):
        self.val = val
        self.another_val = 'some data'
    def __getstate__(self):
        print("I'm being pickled")
        self.val *= 2
        print("val after __getstate__: {}".format(self.val))
        return self.__dict__
    def __setstate__(self, d):
        print("I'm being unpickled with these values: {}".format(d))
        self.__dict__ = d
        self.val *= 3
        print("val after __setstate__: {}".format(self.val))

f = Foo()
f_string = pickle.dumps(f)
f_new = pickle.loads(f_string)
a = f.__dict__
del a["another_val"]
f.__dict__ = a
print(f.__dict__)