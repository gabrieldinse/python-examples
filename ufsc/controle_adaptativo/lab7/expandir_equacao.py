# Author: Gabriel Dinse
# File: expandir_equacao
# Date: 11/21/2020
# Made with PyCharm

# Standard Library

# Third party modules
import numpy as np
import sympy as sym

# Local application imports


# Arquivo extra para expandir as multiplicações da equação diofantina
r0 = sym.Symbol('r0')
r1 = sym.Symbol('r1')
s0 = sym.Symbol('s0')
s1 = sym.Symbol('s1')
s2 = sym.Symbol('s2')
z = sym.Symbol('z')

# Atividade 2 -------------------------------------------------
# Equação diofantina para rejeição de perturbação
eq = (1 - 1.801 * z ** -1 + 0.8187 * z ** -2) * (1 - z ** -1) * (r0 + r1 * z ** -1) \
     + z ** -1 * (0.00935 + 0.00875 * z ** -1) * (s0 + s1 * z ** -1 + s2 * z ** -2)
eq = sym.expand(eq)
result = 1 - 1.605 * z ** -1 + 0.6703 * z ** -2
print(eq)
print("=")
print(result)

# Resultados
a = np.array([[1, 0.00935, 0, 0],
              [-2.801, 0.00875, 0.00935, 0],
              [2.6197, 0, 0.00875, 0.00935],
              [-0.8187, 0, 0, 0.00875]])
b = np.array([1.196, -1.9494, 0.8187, 0])
x = np.linalg.solve(a, b)
print(x)
