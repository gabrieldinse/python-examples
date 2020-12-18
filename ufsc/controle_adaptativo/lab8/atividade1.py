# Author: Gabriel Dinse
# File: expandirequacao
# Date: 11/21/2020
# Made with PyCharm

# Standard Library

# Third party modules
import numpy as np
import sympy as sym

# Local application imports


# Arquivo extra para expandir as multiplicações da equação diofantina
b1e = sym.Symbol('b1e')
b2e = sym.Symbol('b2e')
a1e = sym.Symbol('a1e')
a2e = sym.Symbol('a2e')
bm1 = sym.Symbol('bm1')
bm2 = sym.Symbol('bm2')
am1 = sym.Symbol('am1')
am2 = sym.Symbol('am2')

r0 = sym.Symbol('r0')
r1 = sym.Symbol('r1')
s0 = sym.Symbol('s0')
s1 = sym.Symbol('s1')

z = sym.Symbol('z')

# Atividade 1
# Equação diofantina para rejeição de perturbação
eq = (1 + a1e * z ** -1 + a2e * z ** -2) * (r0 + r1 * z ** -1) \
     + z ** -1 * (b1e + b2e * z ** -1) * (s0 + s1 * z ** -1)
result = 1 + am1 * z ** -1 + am2 * z ** -2
print(sym.simplify(sym.expand(eq)))
print("=")
print(result)

eq1 = a1e * r0 + r1 + b1e * s0 - am1
eq2 = a2e * r0 + a1e * r1 +  b2e * s0 + b1e * s1 - am2
eq3 = r0 - 1
eq4 = a2e * r1 + b2e * s1
solution = sym.solve([eq1, eq2, eq3, eq4], (r0, r1, s0, s1))
r0, r1, s0, s1 = solution.values()

r1 = sym.simplify(sym.expand(r1))
s0 = sym.simplify(sym.expand(s0))
s1 = sym.simplify(sym.expand(s1))
print(f"\n\nr1 = {r1}")
print(f"s0 = {s0}")
print(f"s1 = {s1}")