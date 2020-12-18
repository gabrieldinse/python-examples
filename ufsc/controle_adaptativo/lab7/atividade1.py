# Author: Gabriel Dinse
# File: atividade1
# Date: 11/18/2020
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

G = ctl.tf([2], [1, 2, 2])
Gz = ctl.sample_system(G, T, method='zoh')
Gd = ctl.tf([8], [1, 4, 8])
Gdz = ctl.sample_system(Gd, T, method='zoh')

# Para verificar mais casas decimais
# print(Gz.den)
# print(Gz.num)

wn_ma = np.sqrt(2)
xi_ma = 2 / (2 * wn_ma)
t1_ma = 5 / (xi_ma * wn_ma)
os_ma = 100 * np.exp(-np.pi * xi_ma / np.sqrt(1 - xi_ma ** 2))

wn_mf = np.sqrt(8)
xi_mf = 4 / (2 * wn_mf)
t1_mf = 5 / (xi_mf * wn_mf)
os_mf = 100 * np.exp(-np.pi * xi_mf / np.sqrt(1 - xi_mf ** 2))

print(f"\nG(z):{Gz}")
print(f"xi MA = {xi_ma:.6}")
print(f"wn MA = {wn_ma:.6}")
print(f"t1% MA= {t1_ma:.6}")
print(f"OS% MA = {os_ma:.6}")

print(f"\n\nGd(z):{Gdz}")
print(f"xi MF = {xi_mf:.6}")
print(f"wn MF = {wn_mf:.6}")
print(f"t1% MF= {t1_mf:.6}")
print(f"OS% MF = {os_mf:.6}")


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


for n in range(len(time)):
    # Malha fechada
    y[n] = 0.00935 * u[n - 1] + 0.00875 * u[n - 2] \
           + 1.801 * y[n - 1] - 0.8187 * y[n - 2]
    ys[n] = 11.136 * y[n] - 8.596 * y[n - 1]
    rt[n] = 3.7326 * r[n] + 3.2727 * r[n - 1] - 0.9358 * rt[n - 1]
    e[n] = rt[n] - ys[n]
    u[n] = e[n] - 0.0919 * u[n - 1]

    # Malha aberta (Foi necessário utilizar maior precisão para acertar o ganho
    # em regime permanente)
    y_ma[n] = 0.00935 * r[n - 1] + 0.008746 * r[n - 2] \
              + 1.8006 * y_ma[n - 1] - 0.8187 * y_ma[n - 2]


# Resultados
mplt.rc('lines', linewidth=1, color='b')
mplt.rc('grid', linestyle='dotted', color='black', linewidth=0.7)
mplt.rc('ytick', labelsize=10)
mplt.rc('xtick', labelsize=10)


### Saída do sistema em malha aberta
fig1 = plt.figure(figsize=(15.5 / 2.54, 10.5 / 2.54))
ax1 = plt.subplot(111)
ajusta_posicao_axes(ax1, [-0.02, 0.02, 0.05, -0.02])

plt.step(time, r, where='post', linestyle="dashed", color="green",
         label="Sinal de referência")
plt.step(time, y_ma, where='post', color='blue',
         label='Saída')
plt.title(f"Saída do sistema em malha aberta",fontsize=14)
plt.xlabel('Tempo (s)', fontsize=10)
plt.ylabel('Valor', fontsize=10)
plt.xlim(left=time[0], right=time[-1])
plt.grid()
plt.legend(loc='best', fontsize=10)
fig1.tight_layout()

# Salvar figura
plt.savefig(f"./figuras/malha_aberta.svg")

### Saída do sistema em malha fechada
fig2 = plt.figure(figsize=(15.5 / 2.54, 10.5 / 2.54))
ax2 = plt.subplot(111)
ajusta_posicao_axes(ax2, [-0.02, 0.02, 0.05, -0.02])

plt.step(time, r, where='post', linestyle="dashed", color="green",
         label="Sinal de referência")
plt.step(time, y, where='post', color='blue',
         label='Saída')
plt.title(f"Saída do sistema em malha fechada\ncom o controlador RST",fontsize=14)
plt.xlabel('Tempo (s)', fontsize=10)
plt.ylabel('Valor', fontsize=10)
plt.xlim(left=time[0], right=time[-1])
plt.grid()
plt.legend(loc='best', fontsize=10)
fig2.tight_layout()

# Salvar figura
plt.savefig(f"./figuras/malha_fechada.svg")

plt.show()