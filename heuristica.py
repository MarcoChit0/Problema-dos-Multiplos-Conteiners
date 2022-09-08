"""
1.  Cria uma população P com M soluções.
2.  Repetir até crtiério de parada ser satisfeito:
    2.1.Criar N novas soluções P' repetidamente:
            SELECIONA(1) um par de soluções (r,t) de P.
            Aplica a RECOMBINAÇÃO: s = R(r,t).
            Aplica a MUTAÇÃO: s = M(s).
            s = BuscaLocal(s)
    2.2.SELECIONA(2) uma nova população P entre P, P'.
"""

from copy import deepcopy
from math import ceil, floor
from numpy import *

COUNT = 0
NUM_EXECUCOES = 3

def increment():
    global COUNT
    COUNT = COUNT + 1

# ok
def gera_solucoes(num_itens, num_conteiners, num_solucoes, pesos_conteiners, pesos_itens):
    solucoes = []
    while len(solucoes) < num_solucoes:
        solucoes.append(atribui_itens_aleatoriamente(num_itens, num_conteiners, pesos_conteiners, pesos_itens))
    return solucoes


def atribui_itens_aleatoriamente(num_itens, num_conteiners, pesos_conteiners, pesos_itens):
    atribuicao_itens = [[0 for i in range(num_itens)] for k in range(num_conteiners)]
    print(atribuicao_itens)
    for conteiner in range(num_conteiners):
        for item in range(num_itens):
            if posso_atribuir(atribuicao_itens, item, conteiner, num_itens, num_conteiners, pesos_itens, pesos_conteiners) and (random.choice([0,1], size=1, p=[0.5,0.5])[0] == 1):
                atribuicao_itens[conteiner][item] = 1
    return atribuicao_itens


def posso_atribuir(atribuicao, item, conteiner, num_itens, num_conteiners, pesos_itens, pesos_conteiners):
    sum = 0
    for cont in range(num_conteiners):
        sum += atribuicao[cont][item]
    
    if sum == 0:
        peso_atual = 0
        for i in range(num_itens):
            peso_atual += ( atribuicao[conteiner][i] * pesos_itens[i] )
        if (peso_atual + pesos_itens[item]) <= pesos_conteiners[conteiner]:
            return True
        else:
            return False
    else:
        return False

def criterio_parada_satisfeito():
    increment()
    if COUNT < NUM_EXECUCOES:
        return False
    else:
        return True

def torneio(solucoes, num_participantes_torneio, valores_itens, valores_pares_itens, num_itens, num_conteiners):
    participantes = random.choice(solucoes, size=num_participantes_torneio)
    melhores_participantes = sorted(participantes, key=lambda p: funcao_objetivo(p, valores_itens, valores_pares_itens, num_itens, num_conteiners))
    return melhores_participantes[0], melhores_participantes[1]

def recombinacao(solucao_01, solucao_02, num_particao=1):
    for part in range(num_particao):
        # Troca um conteiner inteiro entre duas soluções.
        # Evita, assim, ficar recalculando o peso para ver se passou ou não do peso máximo do conteiner.
        swap(solucao_01, solucao_02, part)

def swap(lista01, lista02, posic):
    lista01[posic], lista02[posic] = lista02[posic], lista01[posic]

def mutacao(solucao, num_conteiners, num_itens, pesos_itens, pesos_conteiners):
    for conteiner in range(num_conteiners):
        if random.choice([0,1], size=1)[0] == 1:
            item_aleatorio = random.choice(num_itens, size=1)[0]
            if solucao[conteiner][item_aleatorio] == 1:
                solucao[conteiner][item_aleatorio] = 0
            elif(posso_atribuir(solucao, item_aleatorio, conteiner, num_itens, num_conteiners, pesos_itens, pesos_conteiners)):
                solucao[conteiner][item_aleatorio] = 1


# TODO
def busca_local(solucao):
    pass

def selecao(populacao_original, nova_populacao, valores_itens, valores_pares_itens, num_itens, num_conteiners, num_solucoes_populacao_original, alpha=0.1, beta=0.9):
    # alpha = orinal + nova
    pop_alpha = deepcopy(populacao_original)
    pop_alpha.union(deepcopy(nova_populacao))
    pop_alpha = sorted(pop_alpha, key=lambda sol: funcao_objetivo(sol, valores_itens, valores_pares_itens, num_itens, num_conteiners))
    # beta = nova
    pop_beta = sorted(nova_populacao, key=lambda sol: funcao_objetivo(sol, valores_itens, valores_pares_itens, num_itens, num_conteiners))
    num_alpha_solucoes = ceil(alpha*num_solucoes_populacao_original)
    num_beta_solucoes = floor(beta*num_solucoes_populacao_original)
    populacao_final = []
    populacao_final.union(pop_alpha[0:num_alpha_solucoes])
    populacao_final.union(pop_beta[0:num_beta_solucoes])
    return populacao_final
    


# ok
def funcao_objetivo(solucao, valores_itens, valores_pares_itens, num_itens, num_conteiners):
    soma_pares = 0
    for k in range(num_conteiners):
        for i in range(num_itens-1):
            for j in range(num_itens-1):
                if solucao[k][i] == 1 and solucao[k][j+1] == 1 and (i is not (j+1)):
                    soma_pares += valores_pares_itens[i][j+1]

    soma_itens = 0
    for k in range(num_conteiners):
        for i in range(num_itens):
            if solucao[k][i] == 1:
                soma_itens += valores_itens[i]

    return soma_itens + soma_pares    

def heuristica(
    num_itens, 
    num_conteiners, 
    num_solucoes_populacao_original, 
    pesos_conteiners,
    pesos_itens,
    num_solucoes_nova_populacao, 
    num_participantes_torneio, 
    valores_itens,
    valores_pares_itens, 
    num_particao=1,
    alpha=0.1, 
    beta=0.9, 
    # gama,
    ):
    populacao_original = gera_solucoes(num_itens, num_conteiners, num_solucoes_populacao_original, pesos_conteiners, pesos_itens)
    while not criterio_parada_satisfeito():
        nova_populacao = gera_solucoes(num_itens, num_conteiners, num_solucoes_nova_populacao)
        sol_01, sol_02 = torneio(populacao_original, num_participantes_torneio, valores_itens, valores_pares_itens, num_itens, num_conteiners)
        recombinacao(sol_01, sol_02, num_particao)
        mutacao(sol_01)
        mutacao(sol_02)
        # valor_sol_01 = busca_local(sol_01)
        # valor_sol_02 = busca_local(sol_02)
        nova_populacao = selecao(populacao_original, nova_populacao, valores_itens, valores_pares_itens, num_itens, num_conteiners, num_solucoes_populacao_original, alpha, beta)
        # if valor_sol_01 > valor_sol_02:
        #     populacao_original.append(sol_01)
        # else:
        #     populacao_original.append(sol_02)
        if funcao_objetivo(sol_01, valores_itens, valores_pares_itens, num_itens, num_conteiners) > funcao_objetivo(sol_02, valores_itens, valores_pares_itens, num_itens, num_conteiners):
            nova_populacao.append(sol_01)
        else:
            nova_populacao.append(sol_02)
        populacao_original = deepcopy(nova_populacao)
    return populacao_original
# print(heuristica(10, 2, 5, [10, 10], [3,4,5,6,7,2,2,2,4,5], 2, 4))
# print(funcao_objetivo([[1,1,0,0],[0,0,1,0]], [1,2,3,4], [[0,4,1,1],[4,0,1,1],[1,1,0,1],[1,1,1,0]], 4, 2))

