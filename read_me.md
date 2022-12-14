# Problema dos Múltiplos Contêiners

## Instâncias: 
Temos m contêineres com volume Ck, k ∈ [m] e n items com volume Vi e valor
vi, i ∈ [n]. Além disso, cada par de itens tem um valor adicional vij , i, j ∈ [n]. Você
pode assumir que vij = vji.

## Solução:
Uma seleção de itens S ⊆ [n] e uma atribuição desses itens aos contêineres a : S →
[m] que respeita as capacidades, i.e. ∑
i|a(i)=k Vi ≤ Ck.

## Objetivo:
Maximizar o valor total. Cada item selecionado i ∈ S contribui com o seu valor
vi. Além disso, todos pares de itens i, j ∈ S no mesmo contêiner (i.e. a(i) = a(j))
contribuem com o valor vij.

Informações adicionais Instâncias disponíveis em http://www.inf.ufrgs.br/~mrpritt/
oc/pcmcdc.zip. 

As instâncias seguem o seguinte formato:

n <br>
v_1 v_2 ... v_n <br>
v_12 v_13 ... v_1n <br>
v_23 v_24 ... v_2n <br>
v_34 v_35 ... v_3n <br>
... <br>
v_n -2,n-1,v_n -2,n <br>
v_n -1, <br>
0 <br>
na <br>
V_1 V_2 ... V_n <br>

onde “na” pode ser ignorado.

O valor m = 10 é fixo, e os volumes Ck = floor ( 0.8/m * sum Vi for i = 1, ..., n), for k = 1, ..., m.

<br>

## Estrutura do projeto: ##
### in ###
Instâncias do problema.

### out ### 
Resultado dos experimentos. Valores das variáveis e da função objetivo.

### heuristic ###
Resultados das execuções da heurística.

### graphs_data ###
Imagens dos gráficos dos melhores valores e dos valores das médias ao rodar a heurística.

### form ### 
Formulação matemática esecífica de cada uma das instâncias.

### trabalho_final.py ### 
Código em pyhton utilizando pulp como "FrontEnd" e CPLEX como "BackEnd".

### formulacao_matematica.jpeg ###
Imagem da formulação matemática do problema.

### heuristica.py ###
Código em python utilizado para rodar a heurística. Rodei a heurística uma vez para cada instância do problema, onde o código foi executado 10 vezes, alterando o tamanho da população original. Depois, os resultados foram armazenados em heuristic

### plot_graph.py ###
Código em python utilizado para plotar os gráficos com base nos dados obtidos em heuristica.py.

### h_specs_pc.html ###
Confirgurações do computador utilizado para rodar as instâncias da heurística, utilizando Ubuntu 20.04.

### fm_specs_pc.html ###
Confirgurações do computador utilizado para rodar as instâncias da formulação matemática, utilizando Ubuntu 20.04.

### apresentacao.pdf ###
PDF de apresentação a ser utilizado em aula.

### INF05010 Otimização Combinatória ###
PDF de relatório, contando a minha implementação da heurística e os resultados obtidos.

### read_me.md ### 
Arquivo de auxílio.

### resultados.txt ###
Arquivo comparando o resultado encontrado da formulação matemática com o melhor valor conhecido para cada instância.
