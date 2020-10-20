# Author: Gabriel Dinse
# File: parte6_segunda_ordem
# Date: 10/1/2020
# Made with PyCharm

# Standard Library
import numpy as np
import control as ctl
import matplotlib.pyplot as plt

# Third party modules


# Local application imports


# Continuous system
K = 2
wn = 20
xi = 0.5
nums = np.array([K * (wn ** 2)])
dens = np.array([1, 2 * xi * wn, wn ** 2])

Gs = ctl.tf(nums, dens)
print(Gs)

# Discrete system
T = 0.1

Gz = ctl.sample_system(Gs, T, method='zoh')
print(Gz)
