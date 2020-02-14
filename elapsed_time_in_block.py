import time

class Timer:
    def __enter__(self):
        self.start_time = time.time()
        
    def __exit__(self, type, value, traceback):
        print ('Elapsed time: {}'.format(time.time() - self.start_time))


with Timer():
    for i in range(100000000):
        pass