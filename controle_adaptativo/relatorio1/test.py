# Author: gabri
# File: test
# Date: 13/03/2020
# Made with PyCharm

# Standard Library
import pickle
import os

# Third party modules
import control as ctl
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib as mplt
import numpy as np

# Local application imports
from step_system_identifier import identify


def adjust_axis_pos(axes, offset):
    box = axes.get_position()
    axes.set_position([box.x0 + offset[0],
                       box.y0 + offset[1],
                       box.width + offset[2],
                       box.height + offset[3]])



plt.close('all')

folder = os.path.dirname(os.path.abspath(__file__))
methods = ["nishikawa", "sundaresan", "smith"]

for filename in os.listdir(folder):
    if filename.endswith('.dat'):
        with open(filename, 'rb') as file:
            data = pickle.load(file)

        fs = data['sampling_frequency']
        A = data['step_amplitude']
        y = data['step_response']

        for method in methods:
            K, tau, L = identify(y, A, fs, method)

            num = np.array([K])
            den = np.array([tau, 1])
            G_est = ctl.tf(num, den)
            t = np.arange(0, len(y) / fs, 1 / fs)
            t_est = np.arange(L, len(y) / fs, 1 / fs)
            _, y_est = ctl.step_response(G_est, t_est)
            y_est = np.append(np.zeros(len(y) - len(y_est)), y_est)

            # Configuracoes de plot
            mplt.rc('lines', linewidth=1, color='b')
            mplt.rc('grid', linestyle='dotted', color='black', linewidth=0.7)
            mplt.rc('ytick', labelsize=9)
            mplt.rc('xtick', labelsize=9)

            fig1 = plt.figure(figsize=(13 / 2.54, 9.5 / 2.54))
            ax1 = plt.subplot(111)
            adjust_axis_pos(ax1, [-0.02, 0.02, 0.05, -0.02])

            plt.step(t, y, where='post')
            plt.title(
                'Método ' + method.capitalize() + ' para o arquivo\n "' +
                filename + '"')
            plt.xlabel('Tempo (s)')
            plt.ylabel('Tensão (V)')
            plt.xlim(left=t[0], right=t[-1])
            plt.grid()
            plt.plot(t, y, color='blue', label='Saída real')
            plt.plot(
                t, y_est, color='red', label='Simulação da planta estimada')
            plt.legend(loc='lower right')
            plt.savefig(method + '_' + os.path.splitext(filename)[0] + '.svg')

        # plt.show()