# Author: Gabriel Dinse
# File: parte9_controlador_dead_bit.py
# Date: 10/27/2020
# Made with PyCharm

# Standard Library

# Third party modules
import numpy as np
import matplotlib.pyplot as plt

# Local application imports


T = 0.1
tmax = 10
t1 = np.arange(0, tmax, T)
umax = 5
umin = -5

# Entrada
sr = np.ones(t1.shape)
sr[t1 > 5] = 2
sr[t1 > 9] = 1

se = np.zeros(t1.size)
su = np.zeros(t1.size)
su_sat = np.zeros(t1.size)
sy = np.zeros(t1.size)

for n in range(t1.size):
    # Planta
    sy[n] = 0.08 * su_sat[n - 5] + 0.9 * sy[n - 1]
    # Erro
    se[n] = sr[n] - sy[n]
    # Controle
    su[n] = 12.5 * se[n] - 11.25 * se[n - 1] + su[n - 5]
    # Saturacao
    su_sat[n] = np.clip(su[n], umin, umax)


# Resultados
plt.figure()
plt.step(t1, sr, where="post")
plt.step(t1, sy, where="post")
plt.show()