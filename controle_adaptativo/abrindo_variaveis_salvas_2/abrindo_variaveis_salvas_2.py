# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 14:15:41 2020

@author: Aluno
"""

import numpy as np
import control as ctl
import pickle
import matplotlib.pyplot as plt


# Abrindo os arquivos
with open('d_step_response_3.dat', 'rb') as file:  # arquivos 1, 2 ou 3
    var = pickle.load(file)

fs = var['sampling_frequency']
A = var['step_amplitude']
y = var['step_response']

plt.plot(y)