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

def step_response_first_order(step_amplitude, gain, time_constant, delay, time_array):
    output = step_amplitude * gain * (1 - np.exp(-(time_array - delay) / time_constant))\
    * np.heaviside(time_array - delay, 1)
    return output


plt.close('all')

folder = os.path.dirname(os.path.abspath(__file__))
methods = ['nishikawa', 'sundaresan', 'smith']

for filename in os.listdir(folder):
    if filename.endswith('.dat'):
        with open(filename, 'rb') as file:
            data = pickle.load(file)

        fs = data['sampling_frequency']
        A = data['step_amplitude']
        y = data['step_response']

        for method in methods:
            k, tau, L = identify_first_order(y, A, fs, method)

            num = np.array([k])
            den = np.array([tau, 1])
            G_est = ctl.tf(num, den)
            print(f"\nMétodo {method.capitalize()}: '{filename}'")
            print(f"Função de transferência: {G_est}")
            print(f"Atraso (L): {L:.6}s\n")

            t = np.arange(0, len(y) / fs, 1 / fs)
            y_est = step_response_first_order(A, k, tau, L, t)

            # Configuracoes de plot
            mplt.rc('lines', linewidth=1, color='b')
            mplt.rc('grid', linestyle='dotted', color='black', linewidth=0.7)
            mplt.rc('ytick', labelsize=9)
            mplt.rc('xtick', labelsize=9)

            fig1 = plt.figure(figsize=(13 / 2.54, 9.5 / 2.54))
            ax1 = plt.subplot(111)
            adjust_axis_pos(ax1, [-0.02, 0.02, 0.05, -0.02])

            plt.step(t, y, where='post')
            plt.title(f'Método {method.capitalize()} para o arquivo\n{filename}"')
            plt.xlabel('Tempo (s)')
            plt.ylabel('Tensão (V)')
            plt.xlim(left=t[0], right=t[-1])
            plt.grid()
            plt.plot(t, y, color='blue', label='Resposta ao degrau: planta real')
            plt.plot(t, y_est, color='red',
                     label='Resposta ao degrau: planta estimada')
            plt.legend(loc='lower right')

            # Salvar a figura na pasta atual
            # plt.savefig(f"{method}_{os.path.splitext(filename)[0]}.svg")

        # Plotar as figuras
        plt.show()