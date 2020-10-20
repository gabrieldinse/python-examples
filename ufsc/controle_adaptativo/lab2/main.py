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
from identify_second_order import identify_second_order


def adjust_axis_pos(axes, offset):
    box = axes.get_position()
    axes.set_position([box.x0 + offset[0],
                       box.y0 + offset[1],
                       box.width + offset[2],
                       box.height + offset[3]])


def step_response_second_order(step_amplitude, gain, damping_ratio,
                               natural_frequency, delay, time, poles):
    if np.issubdtype(poles.dtype, np.dtype(complex)):
        damping_square = (1 - damping_ratio ** 2) ** 0.5
        damped_frequency = natural_frequency * damping_square
        factor = np.exp(-damping_ratio * natural_frequency * (time - delay)) \
                 / damping_square
        output = step_amplitude * gain * (1 - factor * np.sin(damped_frequency * (time - delay) + np.arctan(damping_square / damping_ratio))) \
                 * np.heaviside(time - delay, 1)
        return output
    else:
        tau1 = 1 / pole[0]
        tau2 = 1 / pole[1]
        if tau1 == tau2:
            output = step_amplitude * gain * (1 - np.exp(-(time - delay) / tau1) - (1 / tau1) * (time - delay) * np.exp(-(time - delay) / tau1)) \
                     * np.heaviside(time - delay, 1)
            return output
        else:
            a = tau1 / (tau1 - tau2)
            b = tau2 / (tau2 - tau1)
            output = step_amplitude * gain * (1 - a * np.exp(-(time - delay) / tau1) - b * np.exp(-(time - delay) / tau2)) \
                     * np.heaviside(time - delay, 1)
            return output


plt.close('all')

folder = os.path.dirname(os.path.abspath(__file__))

for i, filename in enumerate(os.listdir(folder), 1):
    if filename.endswith('.dat'):
        with open(filename, 'rb') as file:
            data = pickle.load(file)

        fs = data['sampling_frequency']
        A = data['step_amplitude']
        y = data['step_response']

        k, zeta, wn, L = identify_second_order(y, A, fs)

        num = np.array([k * (wn ** 2)])
        den = np.array([1, 2 * zeta * wn, wn ** 2])
        G_est = ctl.tf(num, den)
        print(f"\n---- Arquivo {filename} ----")
        print(f"Função de transferência: {G_est}")
        print(f"Polos: {G_est.pole()}")
        print(f"Ganho (k): {k:.4}")
        print(f"Coeficiente de amortecimento: {zeta:.4}")
        print(f"Frequência natural: {wn:.4}")
        print(f"Atraso (L): {L:.4}s\n")

        t = np.arange(0, len(y) / fs, 1 / fs)
        y_est = step_response_second_order(A, k, zeta, wn, L, t, G_est.pole())

        # Configuracoes de plot
        mplt.rc('lines', linewidth=1, color='b')
        mplt.rc('grid', linestyle='dotted', color='black', linewidth=0.7)
        mplt.rc('ytick', labelsize=9)
        mplt.rc('xtick', labelsize=9)

        fig1 = plt.figure(figsize=(13 / 2.54, 9.5 / 2.54))
        ax1 = plt.subplot(111)
        adjust_axis_pos(ax1, [-0.02, 0.02, 0.05, -0.02])

        plt.step(t, y, where='post')
        plt.title(f'Arquivo {filename}"')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Tensão (V)')
        plt.xlim(left=t[0], right=t[-1])
        plt.grid()
        plt.plot(t, y, color='blue', label='Resposta ao degrau: planta real')
        plt.plot(t, y_est, color='red',
                 label='Resposta ao degrau: planta estimada')
        plt.legend(loc='lower right')

        # Salvar a figura na pasta atual
        plt.savefig(f"response{i}.svg")

# Plotar as figuras
plt.show()