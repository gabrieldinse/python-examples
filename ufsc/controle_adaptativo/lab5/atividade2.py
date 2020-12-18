# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 08:55:16 2018

@author: Marcos
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mplt
import control as ctl
from scipy import signal
import dsplib


I4 = np.identity(4)


def ajusta_posicao_axes(axes,offset):
    box = axes.get_position()
    axes.set_position([box.x0+offset[0], box.y0+offset[1],
                       box.width+offset[2], box.height+offset[3]])


# Metodos ----------------------------------------------------------------------
def mqr_padrao_iter(x, y, P_ant, theta):
    u = np.array([[x[n - 1]], [x[n - 2]], [-y[n - 1]], [-y[n - 2]]])
    ut = np.transpose(u)
    theta_ant = theta[:, n - 1].reshape(4, 1)

    h = np.matmul(P_ant, u) / (1 + np.matmul(ut, np.matmul(P_ant, u)))
    theta[:, n] = (theta_ant + h * (y[n] - np.matmul(ut, theta_ant))).reshape(4)
    P = np.matmul(I4 - np.matmul(h, ut), P_ant)

    return P

def mqr_reinicializacao_iter(x, y, P_ant, theta, limiar, newP):
    u = np.array([[x[n - 1]], [x[n - 2]], [-y[n - 1]], [-y[n - 2]]])
    ut = np.transpose(u)
    theta_ant = theta[:, n - 1].reshape(4, 1)

    h = np.matmul(P_ant, u) / (1 + np.matmul(ut, np.matmul(P_ant, u)))
    theta[:, n] = (theta_ant + h * (y[n] - np.matmul(ut, theta_ant))).reshape(4)
    erro = (y[n] - np.matmul(np.transpose(u), theta[:, n].reshape(4, 1)))[0][0]

    P = np.matmul(I4 - np.matmul(h, ut), P_ant) if erro <= limiar else newP

    return P

def mqr_fator_esquecimento_iter(x, y, P_ant, theta, fator_esq):
    u = np.array([[x[n - 1]], [x[n - 2]], [-y[n - 1]], [-y[n - 2]]])
    ut = np.transpose(u)
    theta_ant = theta[:, n - 1].reshape(4, 1)

    h = np.matmul(P_ant, u) / (1 + np.matmul(ut, np.matmul(P_ant, u)))
    theta[:, n] = (theta_ant + h * (y[n] - np.matmul(ut, theta_ant))).reshape(4)
    P = (1 / fator_esq) * np.matmul(I4 - np.matmul(h, ut), P_ant)

    return P

# ----------------------------------------------------------------------------
# Sistema 1
K = 1
Wn = 20
Xi = 0.7

num = np.array([K*(Wn**2)])
den = np.array([1, 2*Xi*Wn, Wn**2])

Gs = ctl.tf(num, den)

# Sistema discretizado
fs = 40
T = 1/fs
G0z = ctl.sample_system(Gs, T, method='zoh')

b0_1 = G0z.num[0][0][0]
b0_2 = G0z.num[0][0][1]
a0_1 = G0z.den[0][0][1]
a0_2 = G0z.den[0][0][2]

# Sistema 2
K = 0.95
Wn = 19
Xi = 0.6

num = np.array([K*(Wn**2)])
den = np.array([1, 2*Xi*Wn, Wn**2])

Gs = ctl.tf(num, den)

# Sistema discretizado
fs = 40
T = 1/fs
G1z = ctl.sample_system(Gs, T, method='zoh')

b1_1 = G1z.num[0][0][0]
b1_2 = G1z.num[0][0][1]
a1_1 = G1z.den[0][0][1]
a1_2 = G1z.den[0][0][2]

# ----------------------------------------------------------------------------
# Sinal de entrada x[n]
tmax = 20
time = np.arange(0, tmax, T)

duty = 0.5
f_pwm = 2
x = (signal.square(2*np.pi*f_pwm*time, duty) + 1)/2
    
# Perturbação
sgp2 = 10**-6
p = np.sqrt(sgp2)*np.random.randn(x.size)
    
# Resposta do sistema
y = np.zeros(time.size)

# condições iniciais
x = np.concatenate([x, np.array([0, 0])])
y = np.concatenate([y, np.array([0, 0])])

# ----------------------------------------------------------------------------
# Coeficientes da planta
b1 = b0_1*np.ones(time.size)
b2 = b0_2*np.ones(time.size)
a1 = a0_1*np.ones(time.size)
a2 = a0_2*np.ones(time.size)

b1[time > tmax/2] = b1_1
b2[time > tmax/2] = b1_2
a1[time > tmax/2] = a1_1
a2[time > tmax/2] = a1_2
coefs_reais = [b1, b2, a1, a2]

# ----------------------------------------------------------------------------

# Mínimos Quadrados Recursivo
rho = 5000
fator_esquecimento1 = 0.9
fator_esquecimento2 = 0.95
fator_esquecimento3 = 0.99
limiar1 = 0.004
limiar2 = 0.001
P_ini =  rho * I4

# Para fins de praticidade de simulação e plot
metodos_iteracao = [
    {
        "nome": "MQR Padrão",
        "função": mqr_padrao_iter,
        "nome arquivo": "2_mqr.svg",
        "parâmetros": []
    },
    {
        "nome": f"MQR com reinicialização (limiar = {limiar1})",
        "função": mqr_reinicializacao_iter,
        "nome arquivo": f"2_mqr_limiar_{limiar1}.svg",
        "parâmetros": [limiar1, P_ini]
    },
    {
        "nome": f"MQR com reinicialização (limiar = {limiar2})",
        "função": mqr_reinicializacao_iter,
        "nome arquivo": f"2_mqr_limiar_{limiar2}.svg",
        "parâmetros": [limiar2, P_ini]
    },
    {
        "nome": f"MQR com fator de esquecimento ($\lambda$ = {fator_esquecimento1})",
        "função": mqr_fator_esquecimento_iter,
        "nome arquivo": f"2_mqr_esquecimento_{fator_esquecimento1}.svg",
        "parâmetros": [fator_esquecimento1]
    },
    {
        "nome": f"MQR com fator de esquecimento ($\lambda$ = {fator_esquecimento2})",
        "função": mqr_fator_esquecimento_iter,
        "nome arquivo": f"2_mqr_esquecimento_{fator_esquecimento2}.svg",
        "parâmetros": [fator_esquecimento2]
    },
    {
        "nome": f"MQR com fator de esquecimento ($\lambda$ = {fator_esquecimento3})",
        "função": mqr_fator_esquecimento_iter,
        "nome arquivo": f"2_mqr_esquecimento_{fator_esquecimento3}.svg",
        "parâmetros": [fator_esquecimento3]
    }
]

for metodo in metodos_iteracao:
    P_ant = P_ini
    theta = np.zeros((4, len(time) + 1))

    # Resposta do sistema
    y = np.zeros(len(time))

    # condições iniciais
    x = np.concatenate([x, np.array([0, 0])])
    y = np.concatenate([y, np.array([0, 0])])

    for n in np.arange(0, len(time)):
        # Saída do sistema
        y[n] = b1[n] * x[n - 1] + b2[n] * x[n - 2] \
               - a1[n] * y[n - 1] - a2[n] * y[n - 2] + p[n]

        # MQR
        P_ant = metodo["função"](x, y, P_ant, theta, *metodo["parâmetros"])

    # remove condições iniciais
    theta = theta[:, :-1]
    x = x[:-2]
    y = y[:-2]

    # ------------------------------------------------------------------------
    # Apresentação da evolução dos coeficientes da planta
    coefs = ["b1", "b2", "a1", "a2"]
    cores = ["blue", "orange", "green", "red"]

    mplt.rc('lines', linewidth=1, color='b')
    mplt.rc('grid', linestyle='dotted', color='black', linewidth=0.7)
    mplt.rc('ytick', labelsize=10)
    mplt.rc('xtick', labelsize=10)

    fig1 = plt.figure(figsize=(15.5 / 2.54, 10.5 / 2.54))
    ax1 = plt.subplot(111)
    ajusta_posicao_axes(ax1, [-0.02, 0.02, 0.05, -0.02])
    amostras = list(range(len(time)))

    for i in range(len(coefs)):
        plt.step(amostras, coefs_reais[i], where='post', color=cores[i],
                 linestyle='dashed')
        plt.step(amostras, theta[i, :], where='post', color=cores[i],
                 label=r"Coeficiente $\bf{" + coefs[i] + "}$")

    plt.title(f"Evolução temporal dos coeficientes estimados\n"
              f"para {metodo['nome']}", fontsize=14)
    plt.xlabel('Amostra', fontsize=10)
    plt.ylabel('Valor', fontsize=10)
    plt.xlim(left=amostras[0], right=amostras[-1])
    plt.grid()
    plt.legend(loc='best', fontsize=10)
    fig1.tight_layout()

    # Salvar figura
    plt.savefig(f"./figuras/{metodo['nome arquivo']}")

plt.show()