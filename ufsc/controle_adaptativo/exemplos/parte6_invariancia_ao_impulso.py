# Author: Gabriel Dinse
# File: parte6_discretizacao_de_sisteas_continuos
# Date: 9/29/2020
# Made with PyCharm

# Standard Library

# Third party modules
import numpy as np
import control as ctl
import matplotlib.pyplot as plt

# Local application imports


# Continuous system
nums = np.array(2)
dens = np.array([5, 1])
Gs = ctl.tf(nums, dens)

t1 = np.arange(0, 35, 0.01)
_, h1 = ctl.impulse_response(Gs, t1)
_, y1 = ctl.step_response(Gs, t1)

# Discrete system
numz = np.array([0.4, 0])
denz = np.array([1, -0.8187])
T = 1
Gz = ctl.tf(numz, denz, T)

t2 = np.arange(0, 35, T)
_, h2 = ctl.impulse_response(Gz, t2)
_, y2 = ctl.step_response(Gz, t2)

# Plot results
# Impulse
plt.figure()
plt.plot(t1, h1)
plt.xlabel("Tempo (s)")
plt.ylabel("Resposta ao ipulso")
plt.grid()
plt.xlim(left=t1[0], right=t1[-1])
markerline, stemlines, _ = plt.stem(t2, h2, use_line_collection=True)
markerline.set_color('k')
stemlines.set_color('k')
plt.xlabel("Tempo (s)")
plt.ylabel("Resposta ao ipulso")
plt.grid()
plt.xlim(left=t2[0], right=t2[-1])

# Step
# Step response is different because we generated Gz based on the impulse invariancy
plt.figure()
plt.plot(t1, y1)
plt.xlabel("Tempo (s)")
plt.ylabel("Resposta ao degrau")
plt.grid()
plt.xlim(left=t1[0], right=t1[-1])
markerline, stemlines, _ = plt.stem(t2, y2, use_line_collection=True)
markerline.set_color('k')
stemlines.set_color('k')
plt.xlabel("Tempo (s)")
plt.ylabel("Resposta ao degrau")
plt.grid()
plt.xlim(left=t2[0], right=t2[-1])

plt.show()