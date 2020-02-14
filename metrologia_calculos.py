# Author: gabri
# File: metrologia_calculos
# Date: 26/06/2019
# Made with PyCharm

# Standard Library
from math import sqrt, log10, floor

# Third party modules

# Local application imports


def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)


def main():
    # Peso padrao # # # # # # # # # # # # # # # # # # # # # # # #
    print('COM O PESO PADRAO\n')
    amostras = [50.20, 50.17, 50.18, 50.18, 50.17]
    media = round(sum(amostras) / len(amostras), 2)
    print('media: {}'. format(media))
    u_padrao = 0
    for amostra in amostras:
        u_padrao += (amostra - media) ** 2 / (len(amostras) - 1)

    u_padrao = round(sqrt(u_padrao), 4)
    print('desvio padrao: {}'.format(u_padrao))
    u_repetitividade = round(u_padrao / sqrt(len(amostras)), 4)
    print('incerteza da repetitividade: {}'.format(u_repetitividade))
    u_resolucao = round((0.01 / 2) / sqrt(3), 5)
    print('incerteza da resolucao: {}'.format(u_resolucao))
    u_combinada = round(sqrt(u_repetitividade**2 + u_resolucao**2), 4)
    print('incerteza combinada: {}'. format(u_combinada))

    # Incerteza combinada
    v_repetitividade = len(amostras) - 1
    v_resolucao = float('inf')
    vef = round((u_combinada ** 4 /
                 (u_repetitividade ** 4 / v_repetitividade +
                  u_resolucao ** 4 / v_resolucao)))
    print('vef: {}'.format(vef))

    # Medidas # # # # # # # # # # # # # # # # # # # # # # # #
    print('\n\nCOM AS MEDIDAS COM AGUA:\n')
    amostras = [201.96, 201.05, 200.94, 203.44, 202.44, 206.14, 201.47,
                202.95, 206.68, 200.65, 200.17, 206.76, 205.86]
    media = round(sum(amostras) / len(amostras), 2)
    print('media: {}'.format(media))
    u_padrao = 0
    for amostra in amostras:
        u_padrao += (amostra - media) ** 2 / (len(amostras) - 1)

    u_padrao = round(sqrt(u_padrao), 4)
    print('desvio padrao: {}'.format(u_padrao))
    u_repetitividade = round(u_padrao, 4)
    print('incerteza da repetitividade: {}'.format(u_repetitividade))
    u_resolucao = round((0.01 / 2) / sqrt(3), 5)
    print('incerteza da resolucao: {}'.format(u_resolucao))
    u_combinada = round(sqrt(u_repetitividade ** 2 + u_resolucao ** 2), 4)
    print('incerteza combinada: {}'.format(u_combinada))

    # Incerteza combinada
    v_repetitividade = len(amostras) - 1
    v_resolucao = float('inf')
    vef = round((u_combinada ** 4 /
                 (u_repetitividade ** 4 / v_repetitividade +
                  u_resolucao ** 4 / v_resolucao)))
    print('vef: {}'.format(vef))


if __name__ == "__main__":
    main()
