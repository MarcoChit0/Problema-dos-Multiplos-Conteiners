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

from asyncore import write
from copy import deepcopy
from math import ceil, floor
from statistics import *
import time
from numpy import *

TIME_LIMIT = 20  # 5 horas 
NUM_INSTANCIAS = 2  # 2 execuções
NUM_CONTEINERS = 10 # fixo -- de acordo com o enunciado

# ok
def gera_solucoes(num_itens, num_conteiners, num_solucoes, pesos_conteiners, pesos_itens):
    solucoes = []
    while len(solucoes) < num_solucoes:
        solucoes.append(atribui_itens_aleatoriamente(num_itens, num_conteiners, pesos_conteiners, pesos_itens))
    return solucoes


def atribui_itens_aleatoriamente(num_itens, num_conteiners, pesos_conteiners, pesos_itens):
    atribuicao_itens = [[0 for i in range(num_itens)] for k in range(num_conteiners)]
    for conteiner in range(num_conteiners):
        for item in range(num_itens):
            if posso_atribuir(atribuicao_itens, item, conteiner, num_itens, num_conteiners, pesos_itens, pesos_conteiners) and (random.choice([0,1], size=1, p=[0.5,0.5])[0] == 1):
                atribuicao_itens[conteiner][item] = 1
    return atribuicao_itens


def posso_atribuir(atribuicao, item, conteiner, num_itens, num_conteiners, pesos_itens, pesos_conteiners):
    sum = 0
    # verifica se eu já selecionei o item
    for cont in range(num_conteiners):
        sum += atribuicao[cont][item]
    
    # verifica se tem espaço no conteiner para adicionar o item
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

def criterio_parada_satisfeito(time_start, time_duration):
    return not (time.time() < time_start + time_duration)

def torneio(solucoes, num_participantes_torneio, valores_itens, valores_pares_itens, num_itens, num_conteiners):
    indice_solucoes_participantes = random.choice(len(solucoes), size=num_participantes_torneio)
    participantes = []
    for index in indice_solucoes_participantes:
        participantes.append(deepcopy(solucoes[index]))
    melhores_participantes = sorted(participantes, key=lambda p:funcao_objetivo(p, valores_itens, valores_pares_itens, num_itens, num_conteiners))
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



def busca_local(solucao, num_itens, num_conteiners, pesos_itens, pesos_conteiners):
    for item in range(num_itens):
        if not foi_selecionado(solucao, item, num_conteiners):
            for conteiner in range(num_conteiners):
                if posso_atribuir(solucao, item, conteiner, num_itens, num_conteiners, pesos_itens, pesos_conteiners):
                    solucao[conteiner][item] = 1
                    break

def foi_selecionado(solucao, item, num_conteiners):
    for conteiner in range(num_conteiners):
            if solucao[conteiner][item] == 1:
                return True
    return False



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
    time_duration = TIME_LIMIT
    time_start = time.time()
    while not criterio_parada_satisfeito(time_start, time_duration):
        nova_populacao =  []
        while len(nova_populacao) < len(populacao_original):
            lista_solucoes = torneio(populacao_original, num_participantes_torneio, valores_itens, valores_pares_itens, num_itens, num_conteiners)
            sol_01 = lista_solucoes[0]
            lista_solucoes = torneio(populacao_original, num_participantes_torneio, valores_itens, valores_pares_itens, num_itens, num_conteiners)
            sol_02 = lista_solucoes[0]
            recombinacao(sol_01, sol_02, num_particao)
            mutacao(sol_01, num_conteiners, num_itens, pesos_itens, pesos_conteiners)
            mutacao(sol_02, num_conteiners, num_itens, pesos_itens, pesos_conteiners)
            # melhoria:
            busca_local(sol_01, num_itens, num_conteiners, pesos_itens, pesos_conteiners)
            busca_local(sol_02, num_itens, num_conteiners, pesos_itens, pesos_conteiners)
            nova_populacao.append(sol_01)
            nova_populacao.append(sol_02)
        populacao_original = selecao(populacao_original, nova_populacao, valores_itens, valores_pares_itens, num_itens, num_conteiners, num_solucoes_populacao_original, alpha, beta)
    melhores_individuos = sorted(populacao_original, key=lambda individuo: funcao_objetivo(individuo, valores_itens, valores_pares_itens, num_itens, num_conteiners), reverse=True)
    return melhores_individuos
# print(heuristica(num_itens= 4,  num_conteiners=2, num_solucoes_populacao_original=5, pesos_conteiners=[3, 3], pesos_itens=[1,2,3,4], num_participantes_torneio= 2, valores_itens=[1,2,3,4],valores_pares_itens=[[0,4,1,1],[4,0,1,1],[1,1,0,1],[1,1,1,0]]))

def read_file(file_name, num_conteiners=NUM_CONTEINERS):
    """
        Objetivo: ler o arquivo de instâncias e salvar os dados do problema.
        file_name: string --> nome do arquivo de entrada.
    """
    input_dir = "./in/"
    f = open(input_dir + file_name)
    itens = 0
    counter = 0
    valor_itens = []
    dic_valor_par_itens = {}
    volume_itens = []
    for line in f.readlines():
        if counter == 0:
            # linha 0 = número de itens
            itens = int(line) 
        elif counter == 1: 
            # linha 1 = valor dos itens
            valor_itens = [int(s)  for s in line.split(" ") if s != "\n"]
        elif 2 <= counter <= itens: 
            # linhas [2, número de itens] = valor dos pares de itens
            dic_valor_par_itens[counter-2] = [int(s)  for s in line.split(" ") if s != "\n"]
        elif counter == itens + 4:
            # linha número de itens + 4 = volume dos itens
            volume_itens = [int(s)  for s in line.split(" ") if s != "\n"]
        counter += 1
    f.close()

    # transformar o dicinário de valores de pares de itens (obtido das linhas [2, número de itens]) em uma matriz simétrica de valores
    coluna = 1
    valor_par_itens = [[0 for i in range(itens)] for j in range(itens)]
    for key in dic_valor_par_itens:
        it_coluna = deepcopy(coluna)
        linha = deepcopy(key)
        for valor in dic_valor_par_itens[key]:
            if it_coluna == linha:
                valor_par_itens[linha][it_coluna] = 0
            else:
                valor_par_itens[linha][it_coluna] = valor
                valor_par_itens[it_coluna][linha] = valor
            it_coluna += 1
        coluna += 1
    
    # volume dos contêiners de acordo com o enunciado do problema
    volume_conteiners = [floor((0.8/num_conteiners) * sum(volume_itens)) for k in range(num_conteiners)]
    return itens, valor_itens, valor_par_itens, volume_itens, volume_conteiners


def main():
    variacoes = [1,2,3,4,5]
    for n in range(NUM_INSTANCIAS):
        # recupera os dados dos arquivos de entrada
        file_name = "pcmcdc" + str(n+1) + ".txt"
        itens, valores, pares, volumes, conteiners = read_file(file_name)
        # para cada uma das alterações no parâmetro: rodar a heuristica, salvar dados. Por fim, realizar a média.
        melhores_individuos = {}    # dicionário de listas.
        for variacao in variacoes:
            random.seed(seed=variacao)                      # [1, 2, ..., 5]
            num_solucoes_populacao_original = 50*variacao   # [50, 100,..., 250]
            num_participantes_torneio = 5*variacao          # [5, 10, ..., 25]
            num_particao = random.choice(NUM_CONTEINERS-1, size=1)[0]
            mais_bem_adaptados = heuristica(num_itens=itens,num_conteiners=NUM_CONTEINERS,valores_itens=valores, valores_pares_itens=pares, pesos_itens=volumes, pesos_conteiners=conteiners, num_solucoes_populacao_original=num_solucoes_populacao_original, num_participantes_torneio=num_participantes_torneio, num_particao=num_particao)
            melhores_individuos[variacao] = mais_bem_adaptados
        write_file(melhores_individuos=melhores_individuos, file_name=file_name, valores_pares_itens=pares, num_itens=itens, valores_itens=valores)


def write_file(melhores_individuos, file_name, valores_pares_itens, num_itens, valores_itens):
    out_dir = "./heuristic/"
    out_pref = "out_heuristic_"
    file = open(out_dir + out_pref + file_name, "w")
    medias = []
    for variacao in melhores_individuos:
        valores = [funcao_objetivo(ind, valores_itens=valores_itens, valores_pares_itens=valores_pares_itens, num_itens=num_itens, num_conteiners=NUM_CONTEINERS) for ind in melhores_individuos[variacao]]
        file.write("variação: "+str(variacao)+"\n")
        file.write("melhor valor: "+str(valores[0])+"\n")
        file.write("média: "+str(mean(valores))+"\n")
        medias.append(mean(valores))
        file.write("mediana: "+str(median(valores))+"\n")
        file.write("moda: "+str(mode(valores))+"\n")
        file.write("desvio padrão: "+str(stdev(valores))+"\n")
        file.write("variância: "+str(pvariance(valores))+"\n")
        file.write("----------------------------------\n")
    file.write("média das médias: " + str(mean(medias)) + "\n")
    file.write("mediana das médias: "+str(median(medias))+"\n")
    file.write("moda das médias: "+str(mode(medias))+"\n")
    file.write("desvio padrão das médias: "+str(stdev(medias))+"\n")
    file.write("variância das médias: "+str(pvariance(medias))+"\n")
    sorted_medias = sorted(medias, reverse=True)
    file.write("melhor valor das médias: "+str(sorted_medias[0])+"\n")
    file.close()    
 
main()        
