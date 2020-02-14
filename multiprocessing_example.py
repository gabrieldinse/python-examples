# Author: Gabriel Dinse
# File: multiprocessing_example
# Date: 07/06/2019
# Made with PyCharm

# Standard Library
from multiprocessing import Process, cpu_count
import time
import os

# Third party modules

# Local application imports


class MuchCPU(Process):
    def run(self):
        print(os.getpid())
        for i in range(200000000):
            pass


if __name__ == '__main__':
    procs = [MuchCPU() for f in range(cpu_count())]
    t = time.time()
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    print('work took {} seconds'.format(time.time() - t))
