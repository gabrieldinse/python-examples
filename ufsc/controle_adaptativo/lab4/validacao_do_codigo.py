# Author: Gabriel Dinse
# File: main
# Date: 10/6/2020
# Made with PyCharm

# Standard Library
import pickle

# Third party modules
import numpy as np
import control as ctl
import matplotlib as mplt
import matplotlib.pyplot as plt

# Local application imports
from identify_least_squares import identify_least_squares


def adjust_axis_pos(axes, offset):
    box = axes.get_position()
    axes.set_position([box.x0 + offset[0],
                       box.y0 + offset[1],
                       box.width + offset[2],
                       box.height + offset[3]])


plt.close("all")

with open('mq_sistema_1.dat', 'rb') as file:
    data = pickle.load(file)
fs = data['sample_frequency']
x = data['input']
y = data['output']
print(f"fs: {fs}")
print(f"x shape: {x.shape}")
print(f"y shape: {y.shape}")

T = 1 / fs
t = np.arange(0, T * len(x), T)
numz, denz = identify_least_squares(10, x, y,
                                    [False, True, True],
                                    [False, True, True])
Gz_est = ctl.tf(numz, denz, T)
print("Sistema estimado pelo arquivo mq_sistema_1.dat")
print(Gz_est)

_, y_est, _ = ctl.forced_response(Gz_est, t, x)

mplt.rc('lines', linewidth=1, color='b')
mplt.rc('grid', linestyle='dotted', color='black', linewidth=0.7)
mplt.rc('ytick', labelsize=9)
mplt.rc('xtick', labelsize=9)

fig1 = plt.figure(figsize=(15 / 2.54, 10 / 2.54))
ax1 = plt.subplot(111)
adjust_axis_pos(ax1, [-0.02, 0.02, 0.05, -0.02])


plt.plot(t, x, color='green', label='Entrada do sistema')
plt.plot(t, y, color='blue',
         label='Saída - Planta real')
plt.plot(t, y_est, color='red', label='Saída - Planta estimada')
plt.title(f'Validação do métodos de Mínimos Quadrados')
plt.xlabel('Tempo (s)')
plt.ylabel('Valor')
plt.xlim(left=t[0], right=t[-1])
plt.grid()
plt.legend(loc='lower right')

# Salvar a figura
plt.savefig("./figuras/validacao_do_codigo.svg")

# Plotar as figuras
plt.show()