from numpy import array, zeros, append, amax, empty, full, copy, matrix, insert, arange, sum, max
from random import randint, seed
from matplotlib.pyplot import plot, show, subplots, legend, xlabel, ylabel
from matplotlib.axes import *

from mdp_iteracao_valor import interacao_valor

#**** Modelo de três estados - slides ****
s = array(["Disposto","Normal","Sonolento"])
a = array(["a"])
p = array([[[0.5],[0.5],[0]],[[0.5],[0],[0.5]],[[0],[0.5],[0.5]]])
r = array([4.0,0.0,-8.0])
terminals = array([]) #indice no vetor "s" dos estados terminais
t = array([   #modelo de transicao - armazena o indice do estado alcancado através da acao indicada no vetor (cf. vetor a)
            [[0,1]],  #de Disposto
            [[0,2]],  #de Normal
            [[1,2]],  #de Sonolento
])

m = interacao_valor(s,a,p,r,0.9999,0.001)
print("Convergiu em ", len(m), "passos")
print("Matrix: ", m[len(m)-1])
for i in range(0,len(r)):
   plot(arange(len(m)),m[:,i],label=s[i])
legend(loc='best')
xlabel('Iteração')
ylabel('Utilidade')
show()
