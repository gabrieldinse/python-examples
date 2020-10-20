from numpy import array, zeros, append, amax, empty, full, copy, matrix, insert, \
    arange
from matplotlib.pyplot import plot, show


# S: conjunto de strings representando os nomes dos estados
# A: conjunto de ações
# P: modelo de transicao
# R: recompensas
def interacao_valor(S, A, P, R, gama, erro):
    u = zeros(len(S))  # vector of utilities - initially zero
    u_prime = copy(R)
    u_prime_prime = copy(R)
    primeiro = 1
    ultimo = copy(R)  # inicializa a k-esima iteracao, s.t. k=0
    sigma = 0
    k = 0
    m = matrix([
                   R])  # matriz que armazena a variacao das recompensas nos diversos estados ao longo das iteracoes

    while primeiro == 1 or sigma > erro * ((1 - gama) / gama):
        primeiro = 0
        u = u_prime
        sigma = 0
        # para cada estado
        for i in range(0, len(S)):
            acoes = array(
                [])  # este array guarda o valor esperado do retorno da execução de cada ação em A a partir do estado S[i]
            for a in range(0, len(
                    A)):  # para cada estado, verifica as probabilidades relacionadas a cada uma das ações
                x = 0
                y = 0  # y armazena a recompensa esperada no i-ésimo estado
                for j in range(0, len(S)):
                    x = P[i][j][a] * u_prime[j]  # equivalente a P(j|a,i)*U(j)
                    y = y + x
                acoes = append(acoes, y)
            ultimo[i] = R[i] + gama * amax(
                acoes)  # bellman update: U(i) = R(s) + gamma*reward of the best action
        u_prime_prime = copy(u_prime)  # backing up the last previous rewards
        u_prime = copy(ultimo)  # updating with the current rewards
        m = insert(m, len(m), u_prime, axis=0)
        k = k + 1
        sigma = max(sigma, amax(abs(u_prime - u_prime_prime)))
    return m
