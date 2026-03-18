# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 19:13:34 2025

@author: 39324
"""
#Questa implementazione ha costo O((n+m) logn). Risulta quindi più efficiente nel caso di grafi
#SPARSI, poiche ha costo O(n logn) rispetto a O(n^2) offerto dall'implemenntazione con liste
from heapq import heappush, heappop

def dijkstra(G, s):
    n = len(G)
    distanza = [float('inf')]*n
    padre = [-1]*n
    
    distanza[s] = 0
    padre[s] = s
    H = []                              #questo sarà il nostro heap
    for (nodo, costo) in G[s]:
        heappush(H, (costo, s, nodo))   #per non perdere informazione DOBBIAMO specificare
                                        #anche chi è il chiamante. In questo caso s
    
    while H:
        costo, s, y = heappop(H)
        if padre[y] == -1:
            padre[y] = s
            distanza[y] = costo
            for v, peso in G[y]:
                if padre[v] == -1:
                    nuovo_costo = distanza[y]+peso
                    heappush(H, (nuovo_costo, y, v))
                
    return distanza, padre

#%% La seguente implementazione ha SEMPRE costo O(n^2). Risulta quindi piu efficiente
#   nel caso di grafi DENSI (l'altro algortimo avrebbe costo O(m logn) = O(n^2 logn))
def dijkstra2(G, s):
    n = len(G)
    #per ogni nodo x, lista[x] contiene (definitivo, distanza, padre)
    lista = [(0, float('inf'), -1) for _ in range(n)]
    lista[s] = (1, 0, s)
    
    #metto tutti gli archi nella lista SENZA segnarli definiti
    for y, costo in G[s]:
        lista[y] = (0, costo, s)
        
    while True:
        minimo = float('inf')
        x = -1
        
        #vado alla ricerca del minimo
        for i in range(n):
            if lista[i][0] == 0 and lista[i][1] < minimo:
                minimo, x = lista[i][1], i
        
        #non ho trovato nessun arco valido
        if minimo == float('inf'):
            break
        
        definitivo, costo_x, origine_x = lista[x]
        lista[x] = (1, costo_x, origine_x)
    
        for y, costo_y in G[x]:
            nuovo_costo = minimo+costo_y
            if lista[y][0] == 0 and nuovo_costo < lista[y][1]:
                lista[y] = (0, nuovo_costo, x)
    
    distanza = [costo for (_, costo, _) in lista]
    padre = [x for (_, _, x) in lista]
    return distanza, padre

