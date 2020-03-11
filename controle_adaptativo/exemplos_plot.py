# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 13:39:28 2020

@author: Aluno
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mplt


def adjust_axis_pos(axes, offset):
    box = axes.get_position()
    axes.set_position([box.x0 + offset[0],
                       box.y0 + offset[1],
                       box.width + offset[2],
                       box.height + offset[3]])


t1 = np.arange(0, 5, 0.01)
f1 = 2
y1 = np.sin(2 * np.pi * f1 * t1)

mplt.rc('lines', linewidth=1, color='b')
mplt.rc('grid', linestyle=':', color='black', linewidth=0.5)
mplt.rc('ytick', labelsize=8)
mplt.rc('xtick', labelsize=8)

fig1 = plt.figure(figsize=(10/2.54, 6/2.54))
ax1 = plt.subplot(111)
adjust_axis_pos(ax1, [0.05, 0.06, 0.03, 0.02])

plt.step(t1, y1, where='post')
plt.xlabel('Tempo (s)')
plt.ylabel('Tensão (V)')
plt.xlim(left=t1[0], right=t1[-1])

