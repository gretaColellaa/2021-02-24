from collections import Counter

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):

        self._matches = []
        self._grafo = nx.DiGraph()
        self._nodes = []
        self._idMapPlayers = {}
        self._edges = []
        pass

    def getMatches(self):
        self._matches = DAO.getMatches()
        return self._matches


    def creaGrafo(self, m):
        self._nodes = DAO.getNodi(m)
        self._grafo.add_nodes_from(self._nodes)
        self.getEfficienza(m)
        lista = []
        presente = False
        for p in self._nodes:
            for p2 in self._nodes:
                if  self._idMapPlayers[p][0] != self._idMapPlayers[p2][0]:
                    delta = abs(self._idMapPlayers[p][1] - self._idMapPlayers[p2][1])
                    #if (p,p2,{"weight" : delta}) not in self._edges or (p2,p,{"weight" : delta}) not in self._edges:
                    # if self._grafo.has_edge(p,p2)  or self._grafo.has_edge(p2,p):
                    #     continue
                    # else:
                    if self._idMapPlayers[p][1] > self._idMapPlayers[p2][1]:
                        self._edges.append((p,p2,{"weight" : delta}))
                        lista.append((p,p2))
                    elif self._idMapPlayers[p][1] == self._idMapPlayers[p2][1]:
                        self._edges.append((p2,p,{"weight" : delta}))
                        lista.append((p2, p))

        self._grafo.add_edges_from(self._edges)
        c = []
        # for e in self._edges:
        #     c.append((e[0], e[1]))
        # print(sorted(c))
        # print(len(set(lista)))
        # conteggio = Counter(lista)
        #
        # duplicati = [item for item, count in conteggio.items() if count > 1]
        # print(sorted(duplicati))





    def getEfficienza(self,m):
        for p in self._nodes:
            team, efficienza = DAO.getEfficienza(p,m)[0]
            self._idMapPlayers[p] = team, efficienza

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)

    def getBest(self):
        best = 0
        bestP = None

        for p in self._nodes:
            # if self._idMapPlayers[p][1] > best:
            #     best = self._idMapPlayers[p][1]
            #     bestP = p
            peso_uscenti = sum(data["weight"] for _, _, data in self._grafo.out_edges(p, data=True))
            peso_entranti = sum(data["weight"] for _, _, data in self._grafo.in_edges(p, data=True))
            risultato = peso_uscenti - peso_entranti
            if risultato > best:
                best = risultato
                bestP = p


        # peso_uscenti = sum(data["weight"] for _, _, data in G.out_edges(nodo, data=True))
        #
        # # Somma dei pesi degli archi entranti
        # peso_entranti = sum(data["weight"] for _, _, data in G.in_edges(nodo, data=True))
        #
        # # Calcolo richiesto
        # risultato = peso_uscenti - peso_entranti

        return bestP, best


