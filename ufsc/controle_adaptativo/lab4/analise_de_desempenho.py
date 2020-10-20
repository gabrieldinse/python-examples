# Author: Gabriel Dinse
# File: analise_de_desempenho
# Date: 10/9/2020
# Made with PyCharm

# Standard Library

# Third party modules
import numpy as np
import control as ctl
import matplotlib.pyplot as plt
import matplotlib as mplt
from scipy.signal import square

# Local application imports
from identify_least_squares import identify_least_squares
import dsplib


def adjust_axis_pos(axes, offset):
    box = axes.get_position()
    axes.set_position([box.x0 + offset[0],
                       box.y0 + offset[1],
                       box.width + offset[2],
                       box.height + offset[3]])


plt.close("all")

# Planta
fs = 40
T = 1 / fs
Gs = ctl.tf([100], [1, 14, 100])
Gz = ctl.sample_system(Gs, T, method='zoh')
print("Planta:")
print(Gs)
print("Planta discretizada por zoh:")
print(Gz)
print(" ------------------------\n")

# Sinais de entrada
t = np.arange(0, 20, T)
fpwm = 4
duty = 0.5

signal_step = np.ones(len(t))
signal_sqr = (square(2 * np.pi * fpwm * t, duty) + 1) / 2
signal_prbn = np.random.rand(t.size) >= 0.5  # Pseudo random binary noise

num_amostras = 20

signal_dicts = [
    {
        "nome": "Degrau unitário (primeiras 20 amostras)",
        "nome arquivo": "degrau_primeiras_20.svg",
        "sinal": signal_step,
        "amostra inicial": 0,
        "numero amostras": num_amostras,
    },
    {
        "nome": "Degrau unitário (últimas 20 amostras)",
        "nome arquivo": "degrau_ultimas_20.svg",
        "sinal": signal_step,
        "amostra inicial": len(signal_step) - num_amostras,
        "numero amostras": num_amostras,
    },
    {
        "nome": "Onda quadrada com frequência 4Hz \n(primeiras 20 amostras)",
        "nome arquivo": "quadrada.svg",
        "sinal": signal_sqr,
        "amostra inicial": 0,
        "numero amostras": num_amostras
    },
    {
        "nome": "Sinal PRBS (primeiras 20 amostras)",
        "nome arquivo": "prbs.svg",
        "sinal": signal_prbn,
        "amostra inicial": 0,
        "numero amostras": num_amostras,
    }
]

indx = [False, True, True]
indy = [False, True, True]



### Estimacao itens a), b) e c) ############################################
print("\t ----\n\tEstimação itens a), b) e c)\n\t ----")

for signal in signal_dicts:
    x = signal["sinal"]
    ini = signal["amostra inicial"]
    num_amostras = signal["numero amostras"]

    _, y, _ = ctl.forced_response(Gz, U=x)

    print(f"\nEntrada: {signal['nome']}")

    try:
        num_est, den_est = identify_least_squares(
            num_amostras, x[ini:ini + num_amostras], y[ini:ini + num_amostras],
            indx, indy)
    except np.linalg.LinAlgError as e:
        print("Erro: Não foi possível calcular a matriz inversa")
        print("\n ---------------------------")
        continue

    Gz_est = ctl.tf(num_est, den_est, T)
    _, y_est, _ = ctl.forced_response(Gz_est, U=x)

    print("\nPlanta estimada pelas amostras:")
    print(Gz_est)
    print("\n ---------------------------")

    mplt.rc('lines', linewidth=1, color='b')
    mplt.rc('grid', linestyle='dotted', color='black', linewidth=0.7)
    mplt.rc('ytick', labelsize=9)
    mplt.rc('xtick', labelsize=9)

    fig = plt.figure(figsize=(15 / 2.54, 10 / 2.54))
    axes = plt.subplot(111)
    adjust_axis_pos(axes, [-0.02, 0.02, 0.05, -0.02])

    plt.plot(t, x, color='green', label='Entrada do sistema', alpha=0.55)
    plt.plot(t, y, color='blue', label='Saída - Planta Real')
    plt.plot(t, y_est, color='red', label='Saída - Planta Estimada')
    plt.title(f'{signal["nome"]}', fontsize=14)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Valor')
    plt.xlim(left=t[0], right=t[-1])
    plt.grid()
    plt.legend(loc='lower right')

    # Salvar a figura
    plt.savefig(f"./figuras/{signal['nome arquivo']}")
########################################################################


### Estimacao item d) ##################################################
print("\t ----\n\tEstimação item d)\n\t ----")

del signal_dicts[1]
sgp2 = 10 ** -6
num_estimativas = 25

num_est = np.zeros((num_estimativas, len(indx)))
den_est = np.zeros((num_estimativas, len(indy)))
coefs = ["b1", "b2", "a1", "a2"]

for signal in signal_dicts:
    print(f"\nEntrada: {signal['nome']}")
    for i in range(num_estimativas):
        x = signal["sinal"]
        pert = np.sqrt(sgp2) * np.random.randn(t.size)
        y = dsplib.forced_response(Gz, x, pert)

        try:
            num_est[i], den_est[i] = identify_least_squares(num_amostras, x, y,
                                                      indx, indy)
        except np.linalg.LinAlgError as e:
            print("Erro: Não foi possível calcular a matriz inversa")
            print("\n ---------------------------")
            continue

    b1 = num_est[:, 1]
    b2 = num_est[:, 2]
    a1 = den_est[:, 1]
    a2 = den_est[:, 2]

    num_avg = np.average(num_est, axis=0)
    b1_avg, b2_avg = num_avg[indx]
    den_avg = np.average(den_est, axis=0)
    a1_avg, a2_avg = den_avg[indy]
    avg_coef = np.array([b1_avg, b2_avg, a1_avg, a2_avg])
    print("\nCoeficientes médios: ")
    print(avg_coef)

    coefs_real = np.concatenate([Gz.num[0][0][indx[1:]], Gz.den[0][0][indy]])
    coefs_err = np.abs((avg_coef - coefs_real) * 100 / coefs_real)
    print("\nErro entre a média e o valor real (%)")
    print(coefs_err)

    b1_max, b2_max = np.max(num_est, axis=0)[indx]
    a1_max, a2_max = np.max(den_est, axis=0)[indy]
    max_coef = np.array([b1_max, b2_max, a1_max, a2_max])
    b1_min, b2_min = np.min(num_est, axis=0)[indx]
    a1_min, a2_min = np.min(den_est, axis=0)[indy]
    min_coef = np.array([b1_min, b2_min, a1_min, a2_min])
    print("\nCoeficientes máximos e mínimos: ")
    print(f"Max: {max_coef}")
    print(f"Min: {min_coef}")

    b1_var, b2_var = np.var(num_est, axis=0)[indx]  # Variância
    a1_var, a2_var = np.var(den_est, axis=0)[indy]  # Variância
    var_coef = np.array([b1_var, b2_var, a1_var, a2_var])
    print("\nVariância:")
    print(var_coef)

    Gz_est = ctl.tf(num_avg, den_avg, T)
    print("\nPlanta média estimada pelas amostras:")
    print(Gz_est)
    print("\n ---------------------------")

    mplt.rc('lines', linewidth=1, color='b')
    mplt.rc('grid', linestyle='dotted', color='black', linewidth=0.7)
    mplt.rc('ytick', labelsize=15)
    mplt.rc('xtick', labelsize=15)

    # Plot
    fig, axes = plt.subplots(nrows=2, ncols=2)
    fig.set_size_inches(25 / 2.54, 24.55 / 2.54)
    axes = axes.flat
    adjust_axis_pos(axes[0], [-0.02, 0.4, 0.05, -0.02])
    adjust_axis_pos(axes[1], [-0.02, -0.025, 0.05, -0.02])
    adjust_axis_pos(axes[2], [-0.02, -0.025, 0.05, -0.02])
    adjust_axis_pos(axes[3], [-0.02, -0.025, 0.05, -0.02])

    err_min = np.abs(min_coef - avg_coef)
    err_max = np.abs(max_coef - avg_coef)

    for i in range(len(x_coefs)):
        axes[i].errorbar([x_coefs[i]], [avg_coef[i]], yerr=[[err_min[i]], [err_max[i]]],
                     fmt='None', ecolor='g', capthick=2, capsize=5)
        axes[i].scatter(x_coefs[i], avg_coef[i], label="Est.", s=20, c="g")
        axes[i].scatter(x_coefs[i], coefs_real[i], label="Real", s=20, c="r")
        axes[i].set_xlabel('Coeficiente', fontsize=15)
        axes[i].set_ylabel('Valor', fontsize=15)
        axes[i].set_title(f'Variação do coeficiente {x_coefs[i]}', fontsize=16)
        axes[i].grid()
        axes[i].legend(loc='lower left', fontsize=15)


    fig.suptitle(f'{signal["nome"]}, coeficientes\n das amostras com ruído', fontsize=18)
    fig.tight_layout()
    fig.subplots_adjust(top=0.81)
        
    # Salvar a figura
    # plt.savefig(f"./figuras/coefs_{signal['nome arquivo']}")

# Plotar as figuras
plt.show()