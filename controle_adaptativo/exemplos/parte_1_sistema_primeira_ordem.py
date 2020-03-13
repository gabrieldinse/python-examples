# Author: gabri
# File: parte_1_sistema_primeira_ordem
# Date: 10/03/2020
# Made with PyCharm

# Standard Library

# Third party modules
import control as ctl
import numpy as np
import matplotlib.pyplot as plt

# Local application imports
K = 1
tau = 1
num = np.array([K])
den = np.array([tau, 1])

G = ctl.tf(num, den)

# Resposta ao degrau
t1 = np.arange(0, 8, 0.01)
_, y1 = ctl.step_response(G, t1)

# REsposta ao seno
f0 = 1
x = np.sin(2 * np.pi * f0 * t1)
_, y2, _ = ctl.forced_response(G, t1, x)

plt.close('all')
plt.figure(figsize=(10/2.54, 6/2.54))
plt.plot(t1, y1)
plt.figure(figsize=(10/2.54, 6/2.54))
plt.plot(t1, x)
plt.plot(t1, y2)

def main():
    pass


if __name__ == "__main__":
    main()
