# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 08:55:16 2018

@author: Marcos

Identification of IIR system using RLS algorithm

"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import control as ctl

# Parâmetros gerais
t_max = 20              # intervalo de simulação [0, t_max]
fs = 20                 # frequência de amostragem

# Vetor de tempo
Ts = 1/fs
time = np.arange(0, t_max, Ts)
IT = len(time)

# Planta 
K = 0.9
tau = 5.0
G = ctl.tf([K], [tau, 1])

Gz = ctl.sample_system(G, Ts)
b = Gz.num[0][0][0]
a = Gz.den[0][0][1]

# Comportamento desejado
Kd = 1
taud = 1

Gd = ctl.tf([Kd], [taud, 1])

Gdz = ctl.sample_system(Gd, Ts)
bd = Gdz.num[0][0][0]
ad = Gdz.den[0][0][1]

# Sinal de referência
sr = np.ones(time.shape)
sr[time>5] = 1
sr[time>10] = 0
sr[time>15] = 1

# Estimador MQR
M = 2
lb = 0.98
p0 = 5000
P = np.matrix(p0*np.eye(M))
K = np.matrix(np.zeros((M,M)))

buffer = np.matrix(np.zeros((M,1)))
parametros = np.matrix(np.zeros((M,IT)))

parametros[0,-1] = 1
parametros[1,-1] = 0

e = np.zeros(IT)
yw = np.zeros(IT)

# Sinais
yp = np.zeros(time.shape)
ys = np.zeros(time.shape)
rt = np.zeros(time.shape)
se = np.zeros(time.shape)
su = np.zeros(time.shape)


# Iterações
for k in np.arange(0,time.size):
    
    # saída da planta
    yp[k] = b * su[k-1] - a * yp[k-1]
   
    # estimador MQR
    buffer = np.transpose(np.matrix([su[k-1], -yp[k-1]]))
        
    e[k] = yp[k] - buffer.T * parametros[:,k-1]
        
    K = P*buffer/(lb + buffer.T * P * buffer)
    parametros[:,k] = parametros[:,k-1] + K*e[k]
        
    P = (1/lb)*(P - K * buffer.T * P)
        
    # parâmetros da planta
    b_e = parametros[0,k]
    a_e = parametros[1,k]
    
    # blocos S(z) e T(z)
    ys[k] = ((ad - a_e) / b_e) * yp[k]
    rt[k] = (bd / b_e) * sr[k]
    
    # sinal de erro
    se[k] = rt[k] - ys[k]

    # bloco 1/R(z)
    su[k] = se[k]
        
    
# ------- RESULTADOS ------- 
plt.figure()
plt.plot(time, sr)
plt.plot(time, yp)
#
# plt.figure()
# plt.step(time, parametros[0, :], where="post")

plt.show()