# Author: Gabriel Dinse
# File: parte6_simulacao_resposta_manual
# Date: 10/1/2020
# Made with PyCharm

# Standard Library

# Third party modules
import numpy as np
import control as ctl
import matplotlib.pyplot as plt

# Local application imports

# Continuous  system
nums = np.array(2)
dens = np.array([5, 1])
Gs = ctl.tf(nums, dens)

t1 = np.arange(0, 35, 0.01)


# Discrete system
T = 1
t2 = np.arange(0, 35, T)

x = np.ones(t2.shape)
x = np.concatenate([x, np.array([0])])
y = np.zeros(t2.shape)
y = np.concatenate([y, np.array([0])])

for n in range(len(x)):
    y[n] = 0.3625 * x[n - 1] + 0.8187 * y[n - 1]

x = x[:-1]
y = y[:-1]

plt.figure()
plt.stem(t2, x, use_line_collection=True)
plt.figure()
plt.stem(t2, y, use_line_collection=True)