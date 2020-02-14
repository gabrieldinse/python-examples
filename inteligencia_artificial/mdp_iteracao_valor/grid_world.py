from numpy import array, zeros, append, amax, empty, full, copy, matrix, insert, \
    arange, sum, max
from random import randint, seed
from matplotlib.pyplot import plot, show, subplots, legend, xlabel, ylabel
from matplotlib.axes import *

from mdp_iteracao_valor import interacao_valor

# **** Modelo de três estados - slides ****
s = array(["(1,1)", "(1,2)", "(1,3)", "(2,1)", "(2,2)", "(2,3)", "(3,1)",
           "(3,2)", "(3,3)", "(4,1)", "(4,2)", "(4,3)"])
a = array(["Up", "Down", "Left", "Right"])
recompensas = array([-0.04, -0.04, -0.04, -0.04, float('nan'), -0.04, -0.04,
                     -0.04, -0.04, -0.04, -1.0, 1.0])

p = array((12, 12, 4, 3))
for i in range(12):
    for j in range(12):
        for k in range(4):
            p[i][j][k][1] = 0.8

p = array([[[0.5], [0.5], [0]], ])
r = array([4.0, 0.0, -8.0])
terminals = array([])  # indice no vetor "s" dos estados terminais
t = array([
    # modelo de transicao - armazena o indice do estado alcancado através da acao indicada no vetor (cf. vetor a)
    [[0, 1]],  # de Disposto
    [[0, 2]],  # de Normal
    [[1, 2]],  # de Sonolento
])

m = interacao_valor(s, a, p, r, 0.1, 0.1)
print("Convergiu em ", len(m), "passos")
print("Matrix: ", m[len(m) - 1])
for i in range(0, len(r)):
    plot(arange(len(m)), m[:, i], label=s[i])
legend(loc='best')
xlabel('Iteração')
ylabel('Utilidade')
show()
