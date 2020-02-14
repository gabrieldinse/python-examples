# Author: gabri
# File: http_client
# Date: 07/09/2019
# Made with PyCharm

# Standard Library
import http.client
import time

# Third party modules

# Local application imports


def main():
    connection = http.client.HTTPSConnection("www.journaldev.com")
    start = time.time()
    for i in range(50):
        connection.request("GET", "/")
        response = connection.getresponse()
        print("Status: {} and reason: {}".format(
            response.status, response.reason))
        read = response.read()
        print(type(read))
    print('{}'.format(time.time() - start))
    connection.close()


if __name__ == "__main__":
    main()
