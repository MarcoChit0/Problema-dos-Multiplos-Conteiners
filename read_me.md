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
v_1 v_2 ... v_n
v_12 v_13 ... v_1n
v_23 v_24 ... v_2n
v_34 v_35 ... v_3n
...
v_n -2,n-1,v_n -2,n
v_n -1,n
0
na
V_1 V_2 ... V_n

onde “na” pode ser ignorado. 

O valor m = 10 é fixo, e os volumes Ck = floor ( 0.8/m * sum Vi for i = 1, ..., n), for k = 1, ..., m.