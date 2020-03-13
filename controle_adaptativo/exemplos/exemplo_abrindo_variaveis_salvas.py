# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 14:10:49 2020

@author: Aluno
"""

import numpy as np
import control as ctl
import pickle


# Abrindo as variaveis
with open('data.dat', 'rb') as file:
    var = pickle.load(file)
    t1 = var['tempo']
    x = var['entrada']
    y = var['saida']