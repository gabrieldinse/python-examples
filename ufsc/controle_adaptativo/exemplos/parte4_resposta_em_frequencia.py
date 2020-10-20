# Author: Gabriel Dinse
# File: parte4_resposta_em_frequencia
# Date: 9/15/2020
# Made with PyCharm

# Standard Library

# Third party modules
import numpy as np
import matplotlib.pyplot as plt
import control as ctl

num = np.array(1)
den = np.array([0.2, 1])
H = ctl.tf(num, den)

# Entrada
f0 = 5
w0 = 2 * np.pi * f0

t1 = np.arange(0, 1.5, 0.005)
x = np.sin(w0 * t1)

# Resposta em frequencia
_, y, _ = ctl.forced_response(H, t1, x)

magnitude = 1 / np.sqrt(1 + 0.04 * (w0 ** 2))
phase = np.arctan(-0.2 * w0)

yp = magnitude * np.sin(w0 * t1 + phase)

# Resultados
plt.figure()
plt.plot(t1, x)
plt.plot(t1, y)
plt.plot(t1, yp)
plt.grid()
plt.xlim(left=t1[0], right=t1[-1])
plt.show()
