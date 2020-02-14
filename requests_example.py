# Author: gabri
# File: requests_example
# Date: 22/08/2019
# Made with PyCharm

# Standard Library
import requests
import threading
import json
import time

# Third party modules

# Local application imports


def main():
    threads = []
    # for i in range(50):
    #     threads.append(
    #         threading.Thread(
    #             target=requests.get,
    #             kwargs={'url': 'https://www.google.com'}))

    start = time.time()
    for i in range(50):
        _ = requests.get(url="http://www.journaldev.com")
    # for thread in threads:
    #     thread.start()
    # for thread in threads:
    #     thread.join()
    print('elapsed: {:.6}'.format(time.time() - start))


if __name__ == "__main__":
    main()
