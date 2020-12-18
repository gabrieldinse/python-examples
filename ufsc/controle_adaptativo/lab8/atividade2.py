# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 08:55:16 2018

@author: Marcos

Identification of IIR system using RLS algorithm

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mplt
import control as ctl


def ajusta_posicao_axes(axes,offset):
    box = axes.get_position()
    axes.set_position([box.x0+offset[0], box.y0+offset[1],
                       box.width+offset[2], box.height+offset[3]])


plt.close('all')


# Parâmetros gerais
t_max = 40  # intervalo de simulação [0, t_max]
fs = 10  # frequência de amostragem

# Vetor de tempo
Ts = 1 / fs
time = np.arange(0, t_max, Ts)
IT = len(time)

# Planta
G = ctl.tf([1.5], [1, 2, 2])
Gz = ctl.sample_system(G, Ts)
b1 = Gz.num[0][0][0]
b2 = Gz.num[0][0][1]
a1 = Gz.den[0][0][1]
a2 = Gz.den[0][0][2]
print(f"\nG(z) = {Gz}")

# Comportamento desejado
Gd = ctl.tf([8], [1, 4, 8])
Gdz = ctl.sample_system(Gd, Ts)
bm1 = Gdz.num[0][0][0]
bm2 = Gdz.num[0][0][1]
am1 = Gdz.den[0][0][1]
am2 = Gdz.den[0][0][2]
print(f"\nGd(z) = {Gdz}")


# Sinal de referência
sr = np.ones(time.shape)
sr[time >= 10] = 0.5
sr[time >= 20] = 1.5
sr[time >= 30] = 0

# Estimador MQR
M = 4
lb = 0.99
p0 = 5000
P = np.matrix(p0 * np.eye(M))
K = np.matrix(np.zeros((M, M)))

buffer = np.matrix(np.zeros((M, 1)))
parametros = np.matrix(np.zeros((M, IT)))

parametros[0, -1] = 0.1
parametros[1, -1] = 0.1
parametros[2, -1] = 0
parametros[3, -1] = 0

e = np.zeros(IT)
yw = np.zeros(IT)

# Sinais
y = np.zeros(time.shape)
y_ma = np.zeros(time.shape)

ys = np.zeros(time.shape)
rt = np.zeros(time.shape)
se = np.zeros(time.shape)
su = np.zeros(time.shape)

# Iterações
for n in np.arange(0, time.size):
    # Saída da planta
    y_ma[n] = b1 * sr[n - 1] + b2 * sr[n - 2] - a1 * y_ma[n - 1] - a2 * y_ma[
        n - 2]

    y[n] = b1 * su[n - 1] + b2 * su[n - 2] \
                - a1 * y[n - 1] - a2 * y[n - 2]
    buffer = np.transpose(
        np.matrix([su[n - 1], su[n - 2], -y[n - 1], -y[n - 2]]))

    # estimador MQR
    e[n] = y[n] - buffer.T * parametros[:, n - 1]

    K = P * buffer / (lb + buffer.T * P * buffer)
    parametros[:, n] = parametros[:, n - 1] + K * e[n]

    P = (1 / lb) * (P - K * buffer.T * P)

    # parâmetros da planta
    b1e = parametros[0, n]
    b2e = parametros[1, n]
    a1e = parametros[2, n]
    a2e = parametros[3, n]

    r0 = 1
    r1 = b2e * (a1e * b2e - a2e * b1e - am1 * b2e + am2 * b1e) / (
            a1e * b1e * b2e - a2e * b1e ** 2 - b2e ** 2)
    s0 = (a1e ** 2 * b2e - a1e * a2e * b1e - a2e * b2e - am1 * (
            a1e * b2e - a2e * b1e) + am2 * b2e) / (
                 -a1e * b1e * b2e + a2e * b1e ** 2 + b2e ** 2)
    s1 = a2e * (a1e * b2e - a2e * b1e - am1 * b2e + am2 * b1e) / (
            -a1e * b1e * b2e + a2e * b1e ** 2 + b2e ** 2)

    # blocos S(z) e T(z)
    ys[n] = s0 * y[n] + s1 * y[n - 1]
    rt[n] = (bm1 / b1e) * sr[n] + (bm2 / b1e) * sr[n - 1] - (b2e / b1e) * \
            rt[n - 1]

    # sinal de erro
    se[n] = rt[n] - ys[n]

    # bloco 1/R(z)
    su[n] = se[n] / r0 - (r1 / r0) * su[n - 1]


# ------- RESULTADOS -------
mplt.rc('lines', linewidth=1, color='b')
mplt.rc('grid', linestyle='dotted', color='black', linewidth=0.7)
mplt.rc('ytick', labelsize=10)
mplt.rc('xtick', labelsize=10)


### Saída do sistema em malha aberta
fig1 = plt.figure(figsize=(15.5 / 2.54, 10.5 / 2.54))
ax1 = plt.subplot(111)
ajusta_posicao_axes(ax1, [-0.02, 0.02, 0.05, -0.02])

plt.step(time, sr, where='post', linestyle="dashed", color="green",
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
# plt.savefig(f"./figuras/malha_aberta.svg")


### Saída do sistema em malha fechada
fig3 = plt.figure(figsize=(15.5 / 2.54, 10.5 / 2.54))
ax3 = plt.subplot(111)
ajusta_posicao_axes(ax3, [-0.02, 0.02, 0.05, -0.02])

plt.step(time, sr, where='post', linestyle="dashed", color="green",
         label="Sinal de referência")
plt.step(time, y, where='post', color='blue',
         label='Saída')
plt.title(f"Saída do sistema em malha fechada\ncom o controlador RST",fontsize=14)
plt.xlabel('Tempo (s)', fontsize=10)
plt.ylabel('Valor', fontsize=10)
plt.xlim(left=time[0], right=time[-1])
plt.grid()
plt.legend(loc='best', fontsize=10)
fig3.tight_layout()

# Salvar figura
# plt.savefig(f"./figuras/malha_fechada.svg")


plt.show()
