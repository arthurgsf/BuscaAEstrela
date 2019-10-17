import pandas as pd
import numpy as np
from arvore import TreeNode
from arvore import Heap

class Mapa:
    def __init__(self, grafo):
        self.__grafo = grafo

    def getHeuristica(self, partida, destino):
        # retorna aqule que não é o -1
        if self.__grafo[partida][destino] == -1:
            return self.__grafo[destino][partida]
        elif self.__grafo[destino][partida] == -1:
            return self.__grafo[partida][destino]
        #caso nenhum dos dois seja -1, retorna o menor (heuristica sempre é menor)
        return min(self.__grafo[partida][destino], self.__grafo[destino][partida])
        
    def getDistancia(self, partida, destino):
        # retorna aqule que é o -1 (ou seja, não há caminho disponível)
        if self.__grafo[partida][destino] == -1:
            return -1
        elif self.__grafo[destino][partida] == -1:
            return -1
        #caso nenhum dos dois seja -1, retorna o maior (valor real sempre é menor)
        return max(self.__grafo[partida][destino], self.__grafo[destino][partida])

    def getVizinhos(self, cidade):
        #pega o triangulo inferior
        triangulo_inf = np.tril(np.ones(self.__grafo.shape)).astype(np.bool)
        vizinhos = self.__grafo.where(triangulo_inf, -1)
        return list(vizinhos[cidade][vizinhos[cidade] > 0].index) + list(vizinhos.loc[cidade][vizinhos.loc[cidade] > 0].index)


def BuscaAEstrela(mapa, partida, destino):
    '''
        Busca A* em um mapa
    '''
    #inicializa a busca a partir do nó de partida
    t = TreeNode({"key":partida, "cost":mapa.getHeuristica(partida, destino)})
    lista = Heap()
    custoAtual = 0
    while(t.data["key"] != destino):
        # adiciona o custo atual + heuristica + custo até o nó
        vizinhos = mapa.getVizinhos(t.data["key"])
        vizinhos = [
            {
                "key":v,
                "cost": custoAtual + mapa.getHeuristica(v, destino) + mapa.getDistancia(t.Key(), v)
            }
            for v in vizinhos
        ]

        # AddChildren retorna os nós inseridos na árvore
        vizinhos = t.AddChildren(vizinhos)

        # monsta uma lista com novos vizinhos
        lista.append(vizinhos)

        # remove o menor da lista e soma o custo real
        newT = lista.pop(lambda x: x.Cost())
        custoAtual += mapa.getDistancia(t.Key(), newT.Key())
        t = newT
    
    #retorna o caminho em uma lista de keys
    caminho = [t.Key()]
    while t.father is not None:
        t = t.father
        caminho.append(t.Key())
    caminho.reverse()
    return caminho
    

if __name__ == "__main__":
    mapa = Mapa(pd.read_csv("grafo.csv", index_col=0).fillna(-1).astype(np.float64))
    partida = input("Cidade de Partida : ")
    destino = input("Cidade de Destino : ")
    caminho = BuscaAEstrela(mapa, partida, destino)
    print("->".join(caminho))