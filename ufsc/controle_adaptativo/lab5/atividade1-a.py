import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mplt
import control as ctl
from scipy import signal
import dsplib

def ajusta_posicao_axes(axes,offset):
    box = axes.get_position()
    axes.set_position([box.x0+offset[0], box.y0+offset[1],
                       box.width+offset[2], box.height+offset[3]])

plt.close("all")

# ----------------------------------------------------------------------------
# Sistema contínuo
num = np.array([400])
den = np.array([1, 28, 400])

Gs = ctl.tf(num, den)

# Sistema discretizado
fs = 40
T = 1/fs
Gz = ctl.sample_system(Gs, T, method='zoh')
print("Função de transferência discretizada:")
print(Gz)

b1 = Gz.num[0][0][0]
b2 = Gz.num[0][0][1]
a1 = Gz.den[0][0][1]
a2 = Gz.den[0][0][2]

# ----------------------------------------------------------------------------
# Sinal de entrada x[n]
tmax = 5
time = np.arange(0, tmax, T)

duty = 0.5
f_pwm = 2
x = (signal.square(2*np.pi*f_pwm*time, duty) + 1)/2

# Perturbação
sgp2 = 10**-6
p = np.sqrt(sgp2)*np.random.randn(len(x))
# ----------------------------------------------------------------------------
# Mínimos Quadrados Recursivo

# (!) Declarar variáveis utilizada aqui
# Coeficientes para plot
b1_arr = b1*np.ones(time.size)
b2_arr = b2*np.ones(time.size)
a1_arr = a1*np.ones(time.size)
a2_arr = a2*np.ones(time.size)
coefs_reais = [b1_arr, b2_arr, a1_arr, a2_arr]

# Variaveis auxiliares
rhos = np.array([5, 500, 5000])
I4 = np.identity(4)

for rho in rhos:
    P_ant = rho * I4  # P inicial
    theta = np.zeros((4, len(time) + 1))

    # Resposta do sistema
    y = np.zeros(len(time))

    # condições iniciais
    x = np.concatenate([x, np.array([0, 0])])
    y = np.concatenate([y, np.array([0, 0])])

    for n in np.arange(0, len(time)):
        # Saída do sistema
        y[n] = b1 * x[n-1] + b2 * x[n-2] - a1 * y[n-1] - a2 * y[n-2] + p[n]

        # MQR
        u = np.array([[x[n - 1]], [x[n - 2]], [-y[n - 1]], [-y[n - 2]]])
        ut = np.transpose(u)
        theta_ant = theta[:, n - 1].reshape(4, 1)

        h = np.matmul(P_ant, u) / (1 + np.matmul(ut, np.matmul(P_ant, u)))
        theta[:, n] = (theta_ant + h * (y[n] - np.matmul(ut, theta_ant))).reshape(4)
        P = np.matmul(I4 - np.matmul(h, ut), P_ant)

        P_ant = P

    # remove condições iniciais
    theta = theta[:,:-1]
    x = x[:-2]
    y = y[:-2]
    
    # ----------------------------------------------------------------------------
    # Função de transferência do sistema estimado, Ge(z)
    numz = theta[:2,-1]
    denz = np.array([1, theta[2, -1], theta[3, -1]])
    Ge = ctl.tf(numz, denz, T)
    print(f"\n\nFunção de transferência estimada para rho = {rho}:")
    print(Ge)
    print(f"Ganho rp: {Ge.dcgain()}")

    # ----------------------------------------------------------------------------
    # Respostas ao degrau
    sinal_degrau = np.ones(time.shape)
    y1_step = dsplib.forced_response(Gz, sinal_degrau, np.zeros(time.shape))
    y2_step = dsplib.forced_response(Ge, sinal_degrau, np.zeros(time.shape))

    # ----------------------------------------------------------------------------
    # Apresentação dos resultados
    ### Curvas de evolução dos coeficientes ###
    coefs = ["b1", "b2", "a1", "a2"]
    cores = ["blue", "orange", "green", "red"]

    mplt.rc('lines', linewidth=1, color='b')
    mplt.rc('grid', linestyle='dotted', color='black', linewidth=0.7)
    mplt.rc('ytick', labelsize=10)
    mplt.rc('xtick', labelsize=10)

    fig1 = plt.figure(figsize=(15.5 / 2.54, 10.5 / 2.54))
    ax1 = plt.subplot(111)
    ajusta_posicao_axes(ax1, [-0.02, 0.02, 0.05, -0.02])
    amostras = list(range(len(time)))

    for i in range(len(coefs)):
        plt.step(amostras, coefs_reais[i], where='post', color=cores[i],
                 linestyle='dashed')
        plt.step(amostras, theta[i, :], where='post',  color=cores[i],
                 label=r"Coeficiente $\bf{" + coefs[i] + "}$")

    plt.title("Evolução temporal dos coeficientes estimados\npara " + r"$\rho = "
              + str(rho) + r"$" + " (Estimação de $2^a$ Ordem)", fontsize=14)
    plt.xlabel('Amostra', fontsize=10)
    plt.ylabel('Valor', fontsize=10)
    plt.xlim(left=amostras[0], right=amostras[-1])
    plt.grid()
    plt.legend(loc='best', fontsize=10)
    fig1.tight_layout()

    # Salvar figura
    plt.savefig(f"./figuras/1a_coefs_rho_{rho}.svg")


    ### Comparação das respostas ###
    mplt.rc('lines', linewidth=1, color='b')
    mplt.rc('grid', linestyle='dotted', color='black', linewidth=0.7)
    mplt.rc('ytick', labelsize=10)
    mplt.rc('xtick', labelsize=10)

    fig2 = plt.figure(figsize=(15.5 / 2.54, 10.5 / 2.54))
    ax2 = plt.subplot(111)
    ajusta_posicao_axes(ax2, [-0.02, 0.02, 0.05, -0.02])

    plt.step(time, y1_step, where='post', color='blue',
             label='Resposta da planta discretizada')
    plt.step(time, y2_step, where='post', color='red',
             label='Resposta da planta estimada')
    plt.step(time, sinal_degrau, where='post', linestyle="dashed", color="green",
             label="Entrada do sistema (degrau unitário)")
    plt.title(f'Comparação das respostas para\n' + r"$\rho = " + str(rho) + r"$"
              + " (Estimação de $2^a$ Ordem)",
              fontsize=14)
    plt.xlabel('Tempo (s)', fontsize=10)
    plt.ylabel('Valor', fontsize=10)
    plt.xlim(left=time[0], right=time[-1])
    plt.grid()
    plt.legend(loc='best', fontsize=10)
    fig2.tight_layout()

    # Salvar figura
    plt.savefig(f"./figuras/1a_degrau_rho_{rho}.svg")

plt.show()



