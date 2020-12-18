# Author: Gabriel Dinse
# File: atividade2
# Date: 11/21/2020
# Made with PyCharm

# Standard Library

# Third party modules
import control as ctl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mplt

# Local application imports


def ajusta_posicao_axes(axes,offset):
    box = axes.get_position()
    axes.set_position([box.x0+offset[0], box.y0+offset[1],
                       box.width+offset[2], box.height+offset[3]])


plt.close("all")


tmax = 40
T = 0.1
time = np.arange(0, tmax, T)

# Sinal referencia
r = np.ones(time.shape)
r[time >= 10] = 0.5
r[time >= 20] = 1.5
r[time >= 30] = 0

rt = np.zeros(time.shape)
ys = np.zeros(time.shape)
e = np.zeros(time.shape)
u = np.zeros(time.shape)
y = np.zeros(time.shape)
y_ma = np.zeros(time.shape)

rt_ = np.zeros(time.shape)
ys_ = np.zeros(time.shape)
e_ = np.zeros(time.shape)
u_ = np.zeros(time.shape)
y_ = np.zeros(time.shape)
y_ma_ = np.zeros(time.shape)

pert = np.zeros(time.shape)
pert[time >= 5] = 1.5
pert[time >= 15] = 0.5
pert[time >= 25] = 1.0
pert[time >= 35] = 1.5


for n in range(len(time)):
    # Malha fechada sem rejeição de perturbação
    y_[n] = 0.00935 * (u_[n - 1] + pert[n - 1]) + 0.00875 * (u_[n - 2] + pert[n - 2]) \
           + 1.801 * y_[n - 1] - 0.8187 * y_[n - 2]
    ys_[n] = 11.136 * y_[n] - 8.596 * y_[n - 1]
    rt_[n] = 3.7326 * r[n] + 3.2727 * r[n - 1] - 0.9358 * rt_[n - 1]
    e_[n] = rt_[n] - ys_[n]
    u_[n] = e_[n] - 0.0919 * u_[n - 1]

    # Malha fechada reprojetado
    y[n] = 0.00935 * (u[n - 1] + pert[n - 1]) + 0.00875 * (u[n - 2] + pert[n - 2]) \
           + 1.801 * y[n - 1] - 0.8187 * y[n - 2]
    ys[n] = 71.4609 * y[n] - 117.2410 * y[n - 1] + 49.3877 * y[n - 2]
    rt[n] = 3.7326 * r[n] + 3.2727 * r[n - 1] - 0.9358 * rt[n - 1]
    e[n] = rt[n] - ys[n]
    u[n] = e[n] + 0.4722 * u[n - 1] + 0.5278 * u[n - 2]


# Resultados
mplt.rc('lines', linewidth=1, color='b')
mplt.rc('grid', linestyle='dotted', color='black', linewidth=0.7)
mplt.rc('ytick', labelsize=10)
mplt.rc('xtick', labelsize=10)

### Saída do sistema em malha fechada com controlador reprojetado
fig1 = plt.figure(figsize=(15.5 / 2.54, 10.5 / 2.54))
ax1 = plt.subplot(111)
ajusta_posicao_axes(ax1, [-0.02, 0.02, 0.05, -0.02])

plt.step(time, pert, where='post', linestyle="dashed", color="red",
         label="Perturbação")
plt.step(time, r, where='post', linestyle="dashed", color="green",
         label="Sinal de referência")
plt.step(time, y, where='post', color='blue',
         label='Saída')
plt.title(f"Saída do sistema com rejeição de\nperturbações do tipo degrau",fontsize=14)
plt.xlabel('Tempo (s)', fontsize=10)
plt.ylabel('Valor', fontsize=10)
plt.xlim(left=time[0], right=time[-1])
plt.grid()
plt.legend(loc='best', fontsize=10)
fig1.tight_layout()

# Salvar figura
plt.savefig(f"./figuras/rejeicao_perturbacao.svg")

### Saída do sistema em malha fechada sem reprojeto
fig2 = plt.figure(figsize=(15.5 / 2.54, 10.5 / 2.54))
ax2 = plt.subplot(111)
ajusta_posicao_axes(ax2, [-0.02, 0.02, 0.05, -0.02])

plt.step(time, pert, where='post', linestyle="dashed", color="red",
         label="Perturbação")
plt.step(time, r, where='post', linestyle="dashed", color="green",
         label="Sinal de referência")
plt.step(time, y_, where='post', color='blue',
         label='Saída')
plt.title(f"Saída do sistema sem rejeição de\nperturbações do tipo degrau", fontsize=14)
plt.xlabel('Tempo (s)', fontsize=10)
plt.ylabel('Valor', fontsize=10)
plt.xlim(left=time[0], right=time[-1])
plt.grid()
plt.legend(loc='best', fontsize=10)
fig2.tight_layout()

# Salvar figura
plt.savefig(f"./figuras/sem_rejeicao_perturbacao.svg")

plt.show()
