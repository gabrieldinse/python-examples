# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 14:21:49 2020

@author: Aluno
"""

import numpy as np


def identify(output, input_amplitude, sampling_rate, method):
    if method == 'sundaresan':
        return _sundaresan(output, input_amplitude, sampling_rate)
    elif method == 'nishikawa':
        return _nishikawa(output, input_amplitude, sampling_rate)
    elif method == 'smith':
        return _smith(output, input_amplitude, sampling_rate)
    else:
        return None, None, None
    

def _sundaresan(output, input_amplitude, sampling_rate):
    flag1 = False
    flag2 = False
    t1 = 0.0
    t2 = 0.0

    for k in range(len(output)):
        if flag1 and flag2:
            break

        if output[k] >= 0.353 * input_amplitude and not flag1:
            t1 = k * sampling_rate
            flag1 = True

        if output[k] >= 0.853 * input_amplitude and not flag2:
            t2 = k * sampling_rate
            flag2 = True

    time_constant = 0.67 * (t2 - t1)
    delay = 1.3 * t1 - 0.29 * t2
    gain = (output[-1] - output[0]) / input_amplitude
    return gain, time_constant, delay


def _nishikawa(output, input_amplitude, sampling_rate):
    pass


def _smith(output, input_amplitude, sampling_rate):
    pass

