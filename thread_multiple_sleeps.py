# Author: gabri
# File: thread_select_system_call
# Date: 11/07/2019
# Made with PyCharm

# Standard Library
from select import select
from threading import Thread
import time


# Third party modules

# Local application imports

def main():
    start = time.time()
    threads = []
    for _ in range(100):
        # args needs to be iterable (list, tupple, etc)
        thread = Thread(target=time.sleep, args=(0.1,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print('Took {:.3} seconds.'.format(time.time() - start))


if __name__ == "__main__":
    main()
