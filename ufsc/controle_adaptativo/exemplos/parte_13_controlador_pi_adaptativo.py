# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 09:08:35 2020

@author: matsu
"""

import numpy as np
import control as ctl
import matplotlib.pyplot as plt

tmax = 100
Ts = 0.1

time = np.arange(0, tmax, Ts)

# Planta
K = 0.8
tau = 4.6

G = ctl.tf([K], [tau, 1])
Gz = ctl.sample_system(G, Ts, method='zoh')

b = Gz.num[0][0][0]
a = Gz.den[0][0][1]

# Especificações de projeto
Xi = 0.5
Wn = 1


# Parâmetros do controlador PI

# Sinais
sr = np.ones(time.shape)
sr[time > 20] = 0
sr[time > 40] = 1
sr[time > 60] = 0
sr[time > 80] = 1

yp = np.zeros(time.shape)
se = np.zeros(time.shape)
su = np.zeros(time.shape)

# Estimador MQR
M = 2
lb = 0.98;
p0 = 5000;
P = np.matrix(p0*np.eye(M))
K = np.matrix(np.zeros((M,M)))

buffer = np.matrix(np.zeros((M,1)))
parametros = np.matrix(np.zeros((M,time.size)))

parametros[0,-1] = 0
parametros[1,-1] = -0.1

e = np.zeros(time.size)

for n in np.arange(time.size):
    
    # Planta
    if n < 5:
        yp[n] = b*sr[n-1] - a*yp[n-1]
        buffer = np.transpose(np.matrix([sr[n-1], -yp[n-1]]))
    else:
        yp[n] = b*su[n-1] - a*yp[n-1]
        buffer = np.transpose(np.matrix([su[n-1], -yp[n-1]]))

    # estimador MQR
    e[n] = yp[n] - buffer.T *parametros[:,n-1]
        
    h = P*buffer/(lb + buffer.T * P * buffer)
    parametros[:,n] = parametros[:,n-1] + h*e[n]
        
    P = (1/lb)*(P - h * buffer.T * P)
        
    # parâmetros da planta
    b_e = parametros[0,n]
    a_e = parametros[1,n]
    
    # Sinal de erro
    se[n] = sr[n] - yp[n]

    # Controlador PI
    tau = -Ts / np.log(-a_e)
    K = b_e / (1 + a_e)

    if n >= 5:
        Kc = (2 * Xi * Wn * tau - 1) / K
        Ti = K * Kc / (tau * (Wn ** 2))

        su[n] = su[n - 1] + Kc * (se[n] - se[n - 1] + (Ts / Ti) * se[n])
    
    
# Resultados
plt.figure()    
plt.step(time, sr, where='post')
plt.step(time, yp, where='post')
plt.xlim(left=time[0], right=time[-1])
plt.ylim(bottom=-0.5, top= 1.5)

plt.figure()
plt.plot(time, su)
plt.show()
    