from copy import deepcopy
from fileinput import filename
from math import floor
from operator import contains
from pulp import *
import numpy as np

num_instancias = 10
num_conteiners = 10 #fixo -- de acordo com o enunciado

def main():
    for n in range(num_instancias):
        # recupera os dados dos arquivos de entrada
        file_name = "pcmcdc" + str(n+1) + ".txt"
        itens, valores, pares, volumes, conteiners = read_file(file_name)
        # monta e executa o programa inteiro
        mult_conteiners(itens, volumes, valores, pares, conteiners, file_name)

def mult_conteiners(num_itens, volumes, valores_itens, valores_pares, conteiners, file_name): 
    """
        Objetivo: monta e executa o programa inteiro.
        num_itens: int --> quantos itens tem no problema.
        volumes: list<int> --> volumes[i] = volume do item i.
        valores_itens: list<int> --> valores_itens[i] = valor do item i.
        valores_pares: list<int> --> valores_pares[i][j] = valor do par de itens (i, j).
        conteiners: list<int> --> conteiners[k] = volume do contêiner k.
        out_file_name: string --> nome do arquivo de saída (onde escreveremos os dados do problema).
    """
    out_pref = "./out/out_"
    form_pref = "./form/LP_out_"

    # construção do modelo
    model = LpProblem("Mult Conteiners", LpMaximize)

    # atribuicao i k = 1 se o item i foi atribuído ao contêiner k
    # atribuicao i k = 0 caso contrário
    atribuicao = LpVariable.dicts(
        "atribuicao", 
        [(i,k) for i in range(num_itens) for k in range(len(conteiners))], 
        cat='Binary'
    )

    # par_atribuido_ao_mesmo_conteiner i j k = 1 se o par de itens i,j foi atribuído ao contêiner k
    # par_atribuido_ao_mesmo_conteiner i j k = 0 caso contrário
    par_atribuido_ao_mesmo_conteiner = LpVariable.dicts(
        "par_atribuido_ao_mesmo_conteiner", 
        [(i,j,k) for i in range(num_itens) for j in range(num_itens) for k in range(len(conteiners))], 
        cat='Binary'
    )
    
    # soma dos valores dos itens selecionados 
    parte1 = lpSum((atribuicao[i, k] * valores_itens[i]) for i in range(num_itens) for k in range(len(conteiners))) 
    # soma dos valores dos pares de itens no mesmo contêiner
    parte2 = lpSum(par_atribuido_ao_mesmo_conteiner[i, j, k] * (valores_pares[i][j]/2) for i in range(num_itens) for j in range(num_itens) for k in range(len(conteiners)))
    # max valor
    model += (
        parte1
        + parte2, "fo")

    # restrições and(atribuicao[i,k], atribuicao[j,k]):
    for k in range(len(conteiners)):
        for j in range(num_itens):
            for i in range(num_itens):
                model += (2*par_atribuido_ao_mesmo_conteiner[i, j, k]) - atribuicao[i, k] - atribuicao[j, k] <= 0
                model += atribuicao[i, k] + atribuicao[j, k] - par_atribuido_ao_mesmo_conteiner[i, j, k] - 1 <= 0


    # um item pode ser estar em apenas um contêiner
    for i in range(num_itens):
        model += lpSum(atribuicao[i,k] for k in range(len(conteiners))) <= 1
    
    # não posso selecionar mais itens do que o contêiner suporta
    for k in range(len(conteiners)):
        model += lpSum((atribuicao[i, k]* volumes[i]) for i in range(num_itens)) <= conteiners[k]

    # limite de tempo (em segundos) = 14400 = 4 h
    time_limit_in_seconds = 60 * 60 * 4
    # solver = CPLEX
    solver = CPLEX_PY(timeLimit=time_limit_in_seconds)
    # rodar experimento
    model.solve(solver)

    # escrever valor das variáveis e da função objetivo no arquivo de saída
    file = open(out_pref + file_name, "w")
    for variable in model.variables():
        file.write(variable.name + " = " + str(variable.varValue) + "\n")
    file.write('model.objective: ' + str(value(model.objective)) + '\n')
    file.write('model.objective.value(): ' + str(value(model.objective.value())) + '\n')
    file.close()

    # escrever formulação no arquivo de formulação
    model.writeLP(form_pref + file_name)



def read_file(file_name):
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

main()
