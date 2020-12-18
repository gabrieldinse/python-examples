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
Kc = (2*Xi*Wn*tau-1)/K
Ti = K*Kc/(tau * (Wn**2))

# Sinais
sr = np.ones(time.shape)
sr[time > 20] = 0
sr[time > 40] = 1
sr[time > 60] = 0
sr[time > 80] = 1

yp = np.zeros(time.shape)
se = np.zeros(time.shape)
su = np.zeros(time.shape)

for n in np.arange(time.size):
    
    # Planta
    yp[n] = b*su[n-1] - a*yp[n-1]
    
    # Sinal de erro
    se[n] = sr[n] - yp[n]
    
    # Controlador PI
    su[n] = su[n - 1] + Kc * (se[n] - se[n - 1] + (Ts / Ti) * se[n])
    
    
    
# Resultados
plt.figure()    
plt.step(time, sr, where='post')
plt.step(time, yp, where='post')

plt.figure()
plt.plot(time, su)

plt.show()