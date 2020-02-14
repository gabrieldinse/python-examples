# Author: Gabriel Dinse
# File: pytest_example
# Date: 25/05/2019
# Made with PyCharm

# Standard Library

# Third party modules

# Local application imports


def setup_module(module):
    print("setting up MODULE {0}".format(
        module.__name__))


def teardown_module(module):
    print("tearing down MODULE {0}".format(
        module.__name__))


def test_a_function():
    print("RUNNING TEST FUNCTION")


class BaseTest:
    @classmethod
    def setup_class(cls):
        print("setting up CLASS {0}".format(
            cls.__name__))

    @classmethod
    def teardown_class(cls):
        print("tearing down CLASS {0}\n".format(
            cls.__name__))

    def setup_method(self, method):
        print("setting up METHOD {0}".format(
            method.__name__))

    def teardown_method(self, method):
        print("tearing down METHOD {0}".format(
            method.__name__))


class TestClass1(BaseTest):
    def test_method_1(self):
        print("RUNNING METHOD 1-1")

    def test_method_2(self):
        print("RUNNING METHOD 1-2")


class TestClass2(BaseTest):
    def test_method_1(self):
        print("RUNNING METHOD 2-1")

    def test_method_2(self):
        print("RUNNING METHOD 2-2")


def main():
    pass


if __name__ == "__main__":
    main()
