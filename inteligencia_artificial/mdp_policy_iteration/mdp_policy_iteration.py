# Implementação do algoritmo Policy-Iteration (cf.Russel and Norvig):
# Dado um MDP, retorna uma política ótima

from numpy import array, zeros, append, amax, empty, full, copy, matrix, insert, \
    arange, sum
from matplotlib.pyplot import plot, show
from random import randint


def policy_evaluation(S, P, R, gama, terminals, pi, k):
    m = matrix([
                   R])  # matriz que armazenara a variacao das recompensas nos diversos estados ao longo das iteracoes
    cont = 0
    while cont < k:
        u = zeros(
            len(S))  # array que vai armazenar as recompensas em cada rodada
        for i in range(0, len(S)):  # percorre todos os estados
            if (i in terminals):
                u[i] = R[i]
            else:
                ultimo = array(
                    m[len(m) - 1][0])  # array com as últimas recompensas
                p = array(P[i])[..., pi[
                    i]]  # array com as probabilidades de atingir cada estado a partir da ação indicada na politica pi
                u[i] = R[i] + gama * sum(ultimo[0] * p)
        m = insert(m, len(m), u, axis=0)
        if cont >= 3 and sum(m[len(m) - 1] - m[len(m) - 2]) == 0 and sum(
                m[len(m) - 2] - m[len(
                        m) - 3]):  # se nas duas ultimas iteracoes não há diferença, convergiu e o algoritmo para
            cont = k
        else:
            cont += 1
    return array(m[len(m) - 1]).flatten()


def policy_iteration(S, A, P, R, gama, terminals, pi, k):
    changed = True
    while changed == True:
        k += 1
        u = policy_evaluation(S, P, R, gama, terminals, pi, k)
        changed = False
        for i in range(0, len(S)):
            a = array(P[i])[..., pi[
                i]]  # array de probabilidades da acao indicada pela politica
            retorno_pi = a * u  # recompensa executando a acao indicada pela politica
            for j in range(0, len(A)):  # para cada ação disponível...
                retorno_a = array(matrix(P[i]).transpose())[
                                j] * u  # ...calcula a recompensa em executar a ação...
                if sum(retorno_a) > sum(
                        retorno_pi):  # ...se a ação examinada têm recompensa maior que a ação indicada pela política....
                    changed = True  # ...a ação indicada pela política é substituída pela ação examinada...
                    pi[i] = j
                    retorno_pi = retorno_a
    return pi
