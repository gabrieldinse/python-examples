# Author: Gabriel Dinse
# File: parte4_diagrama_de_bode
# Date: 9/15/2020
# Made with PyCharm

# Standard Library

# Third party modules
import numpy as np
import matplotlib.pyplot as plt
import control as ctl

# Local application imports


w = np.linspace(0.1, 1500, 10000)
magnitude = 1 / np.sqrt(1 + 0.04 * (w ** 2))
phase = np.arctan(-0.2 * w)
wh = w / (2 * np.pi)
plt.figure()
plt.title("Magnitude")
plt.ylabel("|H(jw)| (dB)")
plt.xlabel("Frequência (Hz)")
plt.semilogx(wh, 20 * np.log10(magnitude))
plt.xlim(left=wh[0], right=wh[-1])
plt.grid()

plt.figure()
plt.ylabel("Fase H(jw) (graus)")
plt.xlabel("Frequência (Hz)")
plt.semilogx(wh, np.degrees(phase))
plt.xlim(left=wh[0], right=wh[-1])
plt.grid()

plt.show()