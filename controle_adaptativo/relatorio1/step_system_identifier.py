# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 14:21:49 2020

@author: Aluno
"""

import numpy as np


def identify(output, input_amplitude, sampling_rate, method):
    """
    :param output: output array
    :param input_amplitude: the input step final value, scalar
    :param sampling_rate: sampling rate (frequency)
    :param method: identify method string: "sundaresan", "nishikawa" or "smith"
    :return: tuple (gain, time constant, delay)
    """
    if method == 'sundaresan':
        return _sundaresan(output, input_amplitude, sampling_rate)
    elif method == 'nishikawa':
        return _nishikawa(output, input_amplitude, sampling_rate)
    elif method == 'smith':
        return _smith(output, input_amplitude, sampling_rate)
    else:
        raise ValueError('Wrong method parameter value.\n"'
                         'Must be: "sundaresan", "nishikawa" or "smith" ')
    

def _sundaresan(output, input_amplitude, sampling_rate):
    flag1 = False
    flag2 = False
    t1 = 0.0
    t2 = 0.0

    for k in range(len(output)):
        if flag1 and flag2:
            break
        if output[k] >= 0.353 * output[-1] and not flag1:
            t1 = k / sampling_rate
            flag1 = True
        if output[k] >= 0.853 * output[-1] and not flag2:
            t2 = k / sampling_rate
            flag2 = True

    gain = (output[-1] - output[0]) / input_amplitude
    time_constant = 0.67 * (t2 - t1)
    delay = 1.3 * t1 - 0.29 * t2
    if delay < 0.0:
        delay = 0.0
    return gain, time_constant, delay


def _nishikawa(output, input_amplitude, sampling_rate):
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
    delay = t0 - time_constant
    if delay < 0.0:
        delay = 0.0
    return gain, time_constant, delay


def _smith(output, input_amplitude, sampling_rate):
    flag1 = False
    flag2 = False
    t1 = 0.0
    t2 = 0.0

    for k in range(len(output)):
        if flag1 and flag2:
            break

        if output[k] >= 0.283 * input_amplitude and not flag1:
            t1 = k / sampling_rate
            flag1 = True

        if output[k] >= 0.632 * input_amplitude and not flag2:
            t2 = k / sampling_rate
            flag2 = True

    time_constant = 1.5 * (t2 - t1)
    gain = (output[-1] - output[0]) / input_amplitude
    delay = t2 - time_constant
    if delay < 0.0:
        delay = 0.0
    return gain, time_constant, delay
