# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 11:27:57 2019

@author: Marcos Matsuo
"""
import numpy as np

def get_numden(Gd, formato='atraso'):
    '''   
    Parâmetros de entrada
        Gd: (control.tf) função de transferência.
        formato: (string) 'atraso' ou 'avanco'.
    
    Retorno
        num: (numpy matrix) coeficientes do numerador.
        den: (numpy matrix) coeficientes do denominador.
    '''    
    
    num = Gd.num[0][0]
    den = Gd.den[0][0]
    
    M = num.size
    N = den.size
    
    if formato == 'atraso':
        num = np.concatenate((np.zeros(N-M),num),axis=0)
        num = np.matrix(np.reshape(num,(N,1)))
        den = np.matrix(np.reshape(den,(N,1)))
        
    elif formato == 'avanco':
        num = np.matrix(num.reshape(M,1)) 
        den = np.matrix(den.reshape(N,1))
            
    return num, den



def forced_response(Gd, x, p):
    '''
    Computa saída de um sistema discreto devido a entrada x[n] e perturbação 
    e[n].
    
    Parâmetros de entrada
        G: (transfer function) função de transferência do sistema discreto
        x: (numpy array) sinal de entrada.
        e: (numpy array) sinal de perturbação.
    
    Retorno
        y: (numpy array) sinal de saída.
    '''
    
    # numerador e denominador
    numz, denz = get_numden(Gd, formato='atraso')
 
    # Saída do sistema
    y = np.zeros(x.shape)

    # Buffers para armazenar amostras dos sinais de entrada e saída
    b_numz = np.matrix(np.zeros((numz.size,1)))
    b_denz = np.matrix(np.zeros((denz.size-1,1)))

    # Iterações
    for n in np.arange(0, x.size):
   
        b_numz[1:] = b_numz[0:-1]
        b_numz[0] = x[n]
    
        y[n] = numz.T * b_numz - denz[1:].T * b_denz + p[n]
    
        b_denz[1:] = b_denz[0:-1]
        b_denz[0] = y[n]
    
    return y
