import matplotlib.pyplot as plt
  
def read_file(file_name):
    dir = "graphs_data/"
    f = open(dir + file_name)
    var = 0
    melhor_valor = 0
    media = 0
    melhores_valores = []
    medias = []
    for line in f.readlines():
        splited_line = line.split(":")
        if(splited_line[0] == "melhor valor"):
            melhor_valor = float(splited_line[1].replace(" ", ""))
        elif(splited_line[0] == "média"):
            media = float(splited_line[1].replace(" ", ""))
            melhores_valores.append(melhor_valor)
            medias.append(media)
    return melhores_valores, medias

def plot_graph(melhores_valores, medias, bkv,file_name):
    plt.clf()
    dir = "graphs_data/"
    bkv_list = [bkv for x in range(10)]
    tamanho_populacao = [50*(x+1) for x in range(10)]
    plt.plot(tamanho_populacao, melhores_valores, label="melhor valor obtido")
    plt.plot(tamanho_populacao, medias, label="medias")
    plt.plot(tamanho_populacao, bkv_list, label="melhor valor conhecido")
    plt.xlabel("tamanho população")
    plt.ylabel("valor da função objetivo")
    plt.title(file_name)
    plt.legend()
    plt.savefig(dir + file_name)

def main():
    bkv = [7992,5985,7604,8610,7132,8935,10984,8154,10385,11958]
    for instancia in range(10):
        file_name = "pcmcdc" + str(instancia+1) 
        melhores_valores, medias = read_file(file_name + ".txt")
        plot_graph(melhores_valores, medias, bkv[instancia] ,file_name + ".png")

main()