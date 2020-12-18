# Author: Gabriel Dinse
# File: parte11_controlador_alocacao_polos
# Date: 11/10/2020
# Made with PyCharm

# Standard Library
import numpy as np
import matplotlib.pyplot as plt

# Third party modules

# Local application imports

tmax = 40
T = 0.1
t1 = np.arange(0, tmax, T)

# Sinal referencia
r = np.ones(t1.shape)

rt = np.zeros(t1.shape)
ys = np.zeros(t1.shape)
e = np.zeros(t1.shape)
u = np.zeros(t1.shape)
y = np.zeros(t1.shape)
y_ma = np.zeros(t1.shape)


for n in range(t1.size):
    y[n] = 0.0198 * u[n-1] + 0.9802 * y[n - 1]
    y_ma[n] = 0.0198 * r[n-1] + 0.9802 * y_ma[n - 1]
    ys[n] = 3.8081 * y[n]
    rt[n] = 4.8061 * r[n]
    e[n] = rt[n] - ys[n]
    u[n] = e[n]

plt.figure()
plt.step(t1, r, where='post')
plt.step(t1, y, where='post')
plt.xlim(left=t1[0], right=t1[-1])
plt.grid()

plt.figure()
plt.step(t1, r, where='post')
plt.step(t1, y_ma, where='post')
plt.xlim(left=t1[0], right=t1[-1])
plt.grid()
plt.show()