# Author: gabri
# File: subprocess_sleep
# Date: 10/07/2019
# Made with PyCharm

# Standard Library
from subprocess import Popen, PIPE
import time

# Third party modules

# Local application imports


def run_sleep(timeout):
    proc = Popen(['sleep', str(timeout)],
                 stdout=PIPE, stdin=PIPE)
    return proc


def main():
    process = Popen(['sleep', '0.3'])
    while process.poll() is None:
        print('Do some work...')
    print('Done!')
    print('Exit status: ', process.poll())

    start = time.time()
    procs = []
    for _ in range(10):
        proc = run_sleep(0.1)
        procs.append(proc)

    # for proc in procs:
    #     proc.communicate()
    end = time.time()
    print('Finished in {:.3f} seconds'.format(end-start))


if __name__ == "__main__":
    main()
