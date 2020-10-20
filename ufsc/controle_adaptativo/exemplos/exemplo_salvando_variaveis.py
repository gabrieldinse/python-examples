# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 13:13:23 2020

@author: Aluno
"""

import numpy as np
import control as ctl
import pickle


# Criacao das variaveis
K = 2
tau = 0.5
num = np.array([K])
den = np.array([tau, 1])
G = ctl.tf(num, den)
t1 = np.arange(0, 5, 0.01)
f0 = 2
x = np.sin(2 * np.pi * f0 * t1)
_, y, _ = ctl.forced_response(G, t1, x)

# Salvando as variaveis
var = {'tempo': t1, 'entrada': x, 'saida': y}

with open('data.dat', 'wb') as file:
    pickle.dump(var, file)
