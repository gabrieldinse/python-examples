# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 14:21:49 2020

@author: Aluno
"""

import numpy as np


def identify(output, input_amplitude, sampling_rate, method):
    if method == 'sundaresan':
        return sundaresan(output, input_amplitude, sampling_rate)
    elif method == 'nishikawa':
        return nishikawa(output, input_amplitude, sampling_rate)
    elif method == 'smith':
        return smith(output, input_amplitude, sampling_rate)
    else:
        raise ValueError('Wrong method parameter value.\n"'
                         'Must be: "sundaresan", "nishikawa" or "smith" ')
    

def sundaresan(output, input_amplitude, sampling_rate):
    k1 = np.where(output >= 0.353 * output[-1])[0][0]
    k2 = np.where(output >= 0.853 * output[-1])[0][0]
    t1 = k1 / sampling_rate
    t2 = k2 / sampling_rate

    gain = (output[-1] - output[0]) / input_amplitude
    time_constant = 0.67 * (t2 - t1)
    delay = max(1.3 * t1 - 0.29 * t2, 0.0)
    return gain, time_constant, delay


def nishikawa(output, input_amplitude, sampling_rate):
    area0 = 0.0
    for k, k_prev in zip(range(1, len(output), 1), range(len(output) - 1)):
        area0 += (output[-1] - (output[k] + output[k_prev]) / 2) / sampling_rate

    time_array = np.arange(
        1 / sampling_rate, len(output) / sampling_rate, 1 / sampling_rate)
    t0 = area0 / (output[-1] - output[0])
    k0 = np.digitize(t0, time_array)

    area1 = 0.0
    for k, k_prev in zip(range(1, int(k0), 1), range(int(k0) - 1)):
        area1 +=  (output[k] + output[k_prev]) / (2 * sampling_rate)
    gain = (output[-1] - output[0]) / input_amplitude
    time_constant = area1 / (0.368 * (output[-1] - output[0]))
    delay = max(t0 - time_constant, 0.0)
    return gain, time_constant, delay


def smith(output, input_amplitude, sampling_rate):s
    k1 = np.where(output >= 0.283 * output[-1])[0][0]
    k2 = np.where(output >= 0.632 * output[-1])[0][0]
    t1 = k1 / sampling_rate
    t2 = k2 / sampling_rate

    time_constant = 1.5 * (t2 - t1)
    gain = (output[-1] - output[0]) / input_amplitude
    delay = max(t2 - time_constant, 0.0)
    return gain, time_constant, delay
