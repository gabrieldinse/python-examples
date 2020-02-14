# Author: Gabriel Dinse
# File: pytest_skipif_decorator
# Date: 29/05/2019
# Made with PyCharm

# Standard Library

# Third party modules
import py.test

# Local application imports


# Skips if python version is under 3.0
@py.test.mark.skipif("sys.version_info <= (3,0)")
def test_python3():
    assert b"hello".decode() == "hello"

# Skips if python version is under 3.7from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
@py.test.mark.skipif("sys.version_info <= (3,7)")
def test_python2():
    assert b"hello".decode() == "hello"


def test_true():
    assert True == True
