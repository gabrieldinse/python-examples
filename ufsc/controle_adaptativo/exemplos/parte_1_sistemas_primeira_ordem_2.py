# Author: gabri
# File: parte_1_sistemas_primeira_ordem_2
# Date: 10/03/2020
# Made with PyCharm

# Standard Library

# Third party modules
import control as ctl
import numpy as np
import matplotlib.pyplot as plt

# Local application imports
K1 = 1
tau1 = 1
K2 = 2
tau2 = 0.5

num1 = np.array([K1])
den1 = np.array([tau1, 1])
num2 = np.array([K2])
den2 = np.array([tau2, 1])

G1 = ctl.tf(num1, den1)
G2 = ctl.tf(num2, den2)
H = ctl.series(G1, G2)

def main():
    pass


if __name__ == "__main__":
    main()
