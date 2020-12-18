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


def mqr_padrao_iter(x, y, n, P_ant, theta):
    u = np.array([[x[n - 1]], [-y[n - 1]]])
    ut = np.transpose(u)
    theta_ant = theta[:, n - 1].reshape(2, 1)

    h = np.matmul(P_ant, u) / (1 + np.matmul(ut, np.matmul(P_ant, u)))
    theta[:, n] = (theta_ant + h * (y[n] - np.matmul(ut, theta_ant))).reshape(2)
    P = np.matmul(np.identity(2) - np.matmul(h, ut), P_ant)

    return P


# Parâmetros gerais
t_max = 40  # intervalo de simulação [0, t_amax]
fs = 20  # frequência de amostragem

# Vetor de tempo
Ts = 1 / fs
time = np.arange(0, t_max, Ts)
IT = len(time)

# Planta discretizada G(z) = b z^-1/(1 + a z^-1)
b = 0.04861
a = -0.94671
Gz = ctl.tf([0, b], [1, a], Ts)
print("Planta real:")
print(Gz)
print(f"Ganho MA: {Gz.dcgain():.6}")
print(f"Tau MA: {-Ts / np.log((Gz.pole()[0])):.6}")
b_real = b * np.ones(time.size)
a_real = a * np.ones(time.size)
coefs_reais = [b_real, a_real]

yp = np.zeros(time.shape)
yp_ma = np.zeros(time.shape)

# Sinal de referência (ALTERAR)
sr = 0.5 * np.ones(time.shape)
sr[time > 10] = 1
sr[time > 20] = 0.75
sr[time > 30] = 1.5

# Estimador MQR
# VARIÁVEIS DO ESTIMADOR MQR
P_ant =  5000 * np.identity(2)
theta = np.zeros((2, len(time) + 1))
# b0 não pode ser zero, a0 não pode ser positivo
theta[:, -1] = [0.5, -0.5]

# Sinais do controlador
se = np.zeros(time.shape)
su = np.zeros(time.shape)

# Especificações do controlador
K_mf = 1
# Não utilizado no loop, pois seu valor já define a equação de diferenças
d = 0

# Iterações
for k in np.arange(0, time.size):
    # saída da planta
    yp[k] = b * su[k - 1] - a * yp[k - 1]
    yp_ma[k] = b * sr[k - 1] - a * yp_ma[k - 1]

    # estimador MQR
    P_ant = mqr_padrao_iter(su, yp, k, P_ant, theta)
    b_est, a_est = theta[:, k]

    # sinal de erro
    se[k] = sr[k] - yp[k]

    # sinal de controle
    tau = -Ts / np.log(-a_est)
    tau_mf = tau / 2
    c = np.exp(-Ts / tau_mf)
    alpha = c + K_mf * (1 - c)
    beta = K_mf * (1 - c) / b_est
    gamma = a_est * K_mf * (1 - c) / b_est

    su[k] =  alpha * su[k - 1] + beta * se[k] + gamma * se[k - 1]

theta = theta[:, :-1]
b_est, a_est = theta[:, -1]
print("\n---------------------------")
print(f"Ganho MA estimado: {b_est / (1 + a_est):.6}")
print(f"Tau MA estimado: {-Ts / np.log(-a_est):.6}")

# ------- RESULTADOS -------
mplt.rc('lines', linewidth=1, color='b')
mplt.rc('grid', linestyle='dotted', color='black', linewidth=0.7)
mplt.rc('ytick', labelsize=10)
mplt.rc('xtick', labelsize=10)


### a) Saída do sistema em malha aberta
fig1 = plt.figure(figsize=(15.5 / 2.54, 10.5 / 2.54))
ax1 = plt.subplot(111)
ajusta_posicao_axes(ax1, [-0.02, 0.02, 0.05, -0.02])

plt.step(time, yp_ma, where='post', color='blue',
         label='Saída')
plt.step(time, sr, where='post', linestyle="dashed", color="green",
         label="Sinal de referência")
plt.title(f"Saída do sistema em malha aberta",fontsize=14)
plt.xlabel('Tempo (s)', fontsize=10)
plt.ylabel('Valor', fontsize=10)
plt.xlim(left=time[0], right=time[-1])
plt.grid()
plt.legend(loc='best', fontsize=10)
fig1.tight_layout()

# Salvar figura
# plt.savefig(f"./figuras/malha_aberta.svg")


### b) Saída do sistema em malha fechada
fig2 = plt.figure(figsize=(15.5 / 2.54, 10.5 / 2.54))
ax2 = plt.subplot(111)
ajusta_posicao_axes(ax2, [-0.02, 0.02, 0.05, -0.02])

plt.step(time, yp, where='post', color='blue',
         label='Saída')
plt.step(time, sr, where='post', linestyle="dashed", color="green",
         label="Sinal de referência")
plt.title(f"Saída do sistema em malha fechada",fontsize=14)
plt.xlabel('Tempo (s)', fontsize=10)
plt.ylabel('Valor', fontsize=10)
plt.xlim(left=time[0], right=time[-1])
plt.grid()
plt.legend(loc='best', fontsize=10)
fig2.tight_layout()

# Salvar figura
# plt.savefig(f"./figuras/malha_fechada.svg")

fig3 = plt.figure(figsize=(15.5 / 2.54, 10.5 / 2.54))
ax3 = plt.subplot(111)
ajusta_posicao_axes(ax3, [-0.02, 0.02, 0.05, -0.02])

plt.step(time, su, where='post', color='blue')
plt.title(f"Sinal de controle",fontsize=14)
plt.xlabel('Tempo (s)', fontsize=10)
plt.ylabel('Valor', fontsize=10)
plt.xlim(left=time[0], right=time[-1])
plt.grid()
fig3.tight_layout()

# Salvar figura
# plt.savefig(f"./figuras/sinal_controle.svg")


### c) Evolução dos coeficientes
coefs = ["b", "a"]
cores = ["blue", "red"]

fig4 = plt.figure(figsize=(15.5 / 2.54, 10.5 / 2.54))
ax4 = plt.subplot(111)
ajusta_posicao_axes(ax4, [-0.02, 0.02, 0.05, -0.02])
amostras = list(range(len(time)))

for i in range(len(coefs)):
    plt.step(amostras, coefs_reais[i], where='post', color=cores[i],
             linestyle='dashed', label=r"$\bf{" + coefs[i] + "}$ real")
    plt.step(amostras, theta[i, :], where='post', color=cores[i],
             label=r"$\bf{" + coefs[i] + "}$ estimado")

plt.title(f"Evolução temporal dos coeficientes estimados", fontsize=14)
plt.xlabel('Amostra', fontsize=10)
plt.ylabel('Valor', fontsize=10)
plt.xlim(left=amostras[0], right=amostras[-1])
plt.grid()
plt.legend(loc='best', fontsize=10)
fig4.tight_layout()

# Salvar figura
# plt.savefig(f"./figuras/coeficientes.svg")

plt.show()