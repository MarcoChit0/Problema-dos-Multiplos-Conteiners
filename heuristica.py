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
NUM_EXECUCOES = 20

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
    indice_solucoes_participantes = random.choice(len(solucoes), size=num_participantes_torneio)
    participantes = []
    for index in indice_solucoes_participantes:
        participantes.append(deepcopy(solucoes[index]))
    melhores_participantes = sorted(participantes, key=lambda p: funcao_objetivo(p, valores_itens, valores_pares_itens, num_itens, num_conteiners))
    return melhores_participantes

def recombinacao(solucao_01, solucao_02, num_particao=1):
    for part in range(num_particao):
        # Troca um conteiner inteiro entre duas soluções.
        # Evita, assim, ficar recalculando o peso para ver se passou ou não do peso máximo do conteiner.
        swap(solucao_01, solucao_02, part)

def atualiza_variaveis(solucao, posic):
    novas_variaveis = []
    count = 0
    for var in solucao[posic]:
        if var == 1:
            novas_variaveis.append(count)
        count += 1

    cont_posic = 0
    for cont in solucao:
        for var_index in novas_variaveis:
            if (cont[var_index] == 1) and (cont_posic != posic):
                cont[var_index] = 0
        cont_posic +=1


def swap(lista01, lista02, posic):
    lista01[posic], lista02[posic] = lista02[posic], lista01[posic]
    atualiza_variaveis(lista01, posic)
    atualiza_variaveis(lista02, posic)


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
    pop_alpha = deepcopy(populacao_original) + deepcopy(nova_populacao)
    pop_alpha = sorted(pop_alpha, key=lambda sol: funcao_objetivo(sol, valores_itens, valores_pares_itens, num_itens, num_conteiners))
    # beta = nova
    pop_beta = sorted(nova_populacao, key=lambda sol: funcao_objetivo(sol, valores_itens, valores_pares_itens, num_itens, num_conteiners))
    num_alpha_solucoes = ceil(alpha*num_solucoes_populacao_original)
    num_beta_solucoes = floor(beta*num_solucoes_populacao_original)
    return pop_alpha[0:int(num_alpha_solucoes)] + pop_beta[0:int(num_beta_solucoes)]
    


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
        #  TODO: gerar pop nova baseada na antiga
        nova_populacao =  []
        while len(nova_populacao) < len(populacao_original):
            sol_01 = torneio(populacao_original, num_participantes_torneio, valores_itens, valores_pares_itens, num_itens, num_conteiners)[0]
            sol_02 = torneio(populacao_original, num_participantes_torneio, valores_itens, valores_pares_itens, num_itens, num_conteiners)[0]
            recombinacao(sol_01, sol_02, num_particao)
            mutacao(sol_01, num_conteiners, num_itens, pesos_itens, pesos_conteiners)
            mutacao(sol_02, num_conteiners, num_itens, pesos_itens, pesos_conteiners)
            # melhoria:
            # valor_sol_01 = busca_local(sol_01)
            # valor_sol_02 = busca_local(sol_02)
            nova_populacao.append(sol_01)
            nova_populacao.append(sol_02)
        populacao_original = selecao(populacao_original, nova_populacao, valores_itens, valores_pares_itens, num_itens, num_conteiners, num_solucoes_populacao_original, alpha, beta)
    return populacao_original
print(heuristica(4, 2, 5, [3, 3], [1,2,3,4], 3, 2, [1,2,3,4],[[0,4,1,1],[4,0,1,1],[1,1,0,1],[1,1,1,0]]))
# print(funcao_objetivo([[1,1,0,0],[0,0,1,0]], [1,2,3,4], [[0,4,1,1],[4,0,1,1],[1,1,0,1],[1,1,1,0]], 4, 2))

# TODO: para cada uma das 10 instâncias do problema dos contêiners: rodar o algoritmo 5 vezes, salvando os resultados, e realizar a média. 
# OBS: para cada vez que eu for rodar o algoritmo, rodar para a mesma semente aleatória, isto é, seed in [1,2,3,4,5].