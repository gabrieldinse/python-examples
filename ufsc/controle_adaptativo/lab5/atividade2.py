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

def ajusta_posicao_axes(axes,offset):
    box = axes.get_position()
    axes.set_position([box.x0+offset[0], box.y0+offset[1],
                       box.width+offset[2], box.height+offset[3]])
    
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

# ----------------------------------------------------------------------------

# Mínimos Quadrados Recursivo
# (!) Declarar variáveis utilizada aqui
rho = np.array([5, 500, 5000])
P_ini =  rho * np.identity(4)



for n in np.arange(0,time.size-1):
    
    # Sistema
    y[n] = b1[n]*x[n-1] + b2[n]*x[n-2] - a1[n]*y[n-1] - a2[n]*y[n-2] + p[n]
    
    # Estimador MQR
    
    # (!) Implementar código do estimador MQR aqui

# remove condições iniciais
x = x[:-2]
y = y[:-2]
    

# ----------------------------------------------------------------------------
# Apresentação da evolução dos coeficientes da planta
