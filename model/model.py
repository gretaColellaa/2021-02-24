import random

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):

        self._matches = []
        self._grafo = nx.DiGraph()
        self._nodes = []
        self._idMapPlayers = {}
        self._edges = []
        self._match = None
        self._azioni = {}
        pass

    def getMatches(self):
        self._matches = DAO.getMatches()
        return self._matches


    def creaGrafo(self, m):
        self._match = m
        self._nodes = DAO.getNodi(m)
        self._grafo.add_nodes_from(self._nodes)
        self.getEfficienza(m)
        lista = []
        presente = False
        for p in self._nodes:
            for p2 in self._nodes:
                if  p!= p2 and self._idMapPlayers[p][0] != self._idMapPlayers[p2][0]:
                    delta = (self._idMapPlayers[p][1] - self._idMapPlayers[p2][1])
                    #if (p,p2,{"weight" : delta}) not in self._edges or (p2,p,{"weight" : delta}) not in self._edges:
                    if self._grafo.has_edge(p,p2) ==False  and self._grafo.has_edge(p2,p)==False:

                    # else:
                        if self._idMapPlayers[p][1] > self._idMapPlayers[p2][1]:
                            self._edges.append((p,p2,{"weight" : delta}))
                            lista.append((p,p2))
                        elif self._idMapPlayers[p][1] < self._idMapPlayers[p2][1]:
                            self._edges.append((p2,p,{"weight" : abs(delta)}))
                            lista.append((p2, p))

        self._grafo.add_edges_from(self._edges)


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
        self._bestP = None

        for p in self._nodes:

            peso_uscenti = sum(data["weight"] for _, _, data in self._grafo.out_edges(p, data=True))
            peso_entranti = sum(data["weight"] for _, _, data in self._grafo.in_edges(p, data=True))
            risultato = peso_uscenti - peso_entranti
            if risultato > best:
                best = risultato
                self._bestP = p


        # peso_uscenti = sum(data["weight"] for _, _, data in G.out_edges(nodo, data=True))
        #
        # # Somma dei pesi degli archi entranti
        # peso_entranti = sum(data["weight"] for _, _, data in G.in_edges(nodo, data=True))
        #
        # # Calcolo richiesto
        # risultato = peso_uscenti - peso_entranti

        return self._bestP, best

    def simula(self, N):
        self._best_team = self._idMapPlayers[self._bestP][0]
        g_h = 11
        g_a= 11
        t_h = DAO.getTeams(self._match)[0]["TeamHomeID"]
        t_a = DAO.getTeams(self._match)[0]["TeamAwayID"]

        self._azioni[t_h] = []
        self._azioni[t_a] = []

        self.ricorsione(N, g_h, g_a, t_h, t_a)
        goal_th = 0
        es_th = 0
        goal_ta=0
        es_ta=0

        for a in self._azioni[t_h]:
            if a == "GOAL":
                goal_th +=1
            if a == "ESPULSO":
                es_th+=1

        for a in self._azioni[t_a]:
            if a == "GOAL":
                goal_ta +=1
            if a == "ESPULSO":
                es_ta+=1

        return (t_h,goal_th,es_th),(t_a,goal_ta, es_ta)



    def ricorsione(self, N,g_h,g_a, t_h, t_a):
        N = int(N)

        if N==0:
            return self._azioni, g_h,g_a
        else:
            i = random.randint(1, 100)
            if i<= 50:
                if g_h>g_a:
                    self._azioni[t_h].append("GOAL")
                elif g_h<g_a:
                    self._azioni[t_a].append("GOAL")
                else:
                    if self._best_team == t_h:
                        self._azioni[t_h].append("GOAL")
                    else:
                        self._azioni[t_a].append("GOAL")
                N = N-1


            elif i>50 and i<=80:
                teams = [t_h,t_a]
                if self._best_team == t_h:
                    prob = [0.6, 0.4]
                else:
                    prob = [0.4, 0.6]

                espulso = random.choices(teams, weights=prob, k=1)[0]
                self._azioni[espulso].append("ESPULSO")
                if espulso == t_h:
                    g_h = g_h-1

                else:
                    g_a = g_a -1

                N = N + random.randint(2,2)
            else:
                infortunio = random.choice(self._nodes)
                team = self._idMapPlayers[infortunio]
                if t_h == team:
                    g_h = g_h-1
                else:
                    g_a = g_a-1
                N=N-1

            self.ricorsione(N,g_h,g_a, t_h,t_a)





