from threading import Timer
import datetime
from urllib.request import urlopen
import pickle
import time


# The two methods __setstate__ and __getstate__ are used by pickle to load
# and dump data from/to files, and should be implemented to use special
# objects with attributes that we can't pickle.

class UpdatedURL:
    def __init__(self, url):
        self.url = url
        self.contents = ''
        self.last_updated = None
        self.update()
    
    # When pickle tries to serialize an object, it simply tries to store 
    # the object's __dict__ attribute. But, before checking __dict__ method,
    # it checks if there is a __getstate__ method, similar to __dict__
    # except that we can exclude attributes that we can't pickle. __getstate__
    # need to return the new attributes list.
    # ** __dict__ is an attribute, not a function, and we can write another
    #    value to it.
    def __getstate__(self):
        new_state = self.__dict__.copy()
        if 'timer' in new_state:
            del new_state['timer']
        return new_state
    
    # data is the dict read from the serial variable after the call to
    # __getstate__. It sets __dict__ to 'data' without the 'timer'
    # attribute, so it needs to insert againt self.timer with the correct
    # date (the time when it was loaded). The 'data' parameter will be
    # initialized with the return of __getstate__ function, in this case, the
    # __dict__ without 'timer' attribute.
    def __setstate__(self, data):
        self.__dict__ = data
        self.schedule()    
        
    def update(self):
        self.contents = urlopen(self.url).read()
        time = datetime.datetime.now()
        self.last_updated = time
        self.schedule()
        
    def schedule(self):
        self.timer = Timer(1, self.update)
        self.timer.setDaemon(True)
        self.timer.start()

a = 1;
def foo():
    t = time.time()
    global a;
    print("{}: {}".format(a, datetime.datetime.now()))
    a += 1
    b = Timer(1 - (time.time() - t), foo)
    b.start()

u = UpdatedURL("https://www.google.com.br")
#b = Timer(1, foo)
#b.start()