# Author: Gabriel Dinse
# File: threading_example_user_input
# Date: 07/06/2019
# Made with PyCharm

# Standard Library
from threading import Thread

# Third party modules

# Local application imports


class InputReader(Thread):
    def run(self):
        self.line_of_text = input()


def main():
    print("Enter some text and press enter: ")
    thread = InputReader()
    thread.start()
    count = 1
    while thread.is_alive():
        count += 1
    print("Incremented up to {0} ".format(count))
    print("while you typed '{}'".format(thread.line_of_text))


if __name__ == "__main__":
    main()
