# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 14:21:49 2020

@author: Aluno
"""

import numpy as np


def identify_second_order(output, input_amplitude, sampling_rate):
    output_steady_state = np.average(output[int(len(output) * 0.95):])
    gain = output_steady_state / input_amplitude
    t15 = np.argmax(output >= 0.15 * output_steady_state) / sampling_rate
    t45 = np.argmax(output >= 0.45 * output_steady_state) / sampling_rate
    t75 = np.argmax(output >= 0.75 * output_steady_state) / sampling_rate
    x = (t45 - t15) / (t75 - t15)
    damping_ratio = (0.0805 - 5.547 * (0.475 - x) ** 2) / (x - 0.356)

    if damping_ratio < 1.0:
        f2 = 0.708 * (2.811 ** damping_ratio)
    else:
        f2 = 2.6 * damping_ratio - 0.6

    natural_frequency = f2 / (t75 - t15)
    fe = 0.922 * (1.66 ** damping_ratio)
    delay = t45 - fe / natural_frequency

    return gain, damping_ratio, natural_frequency, delay

