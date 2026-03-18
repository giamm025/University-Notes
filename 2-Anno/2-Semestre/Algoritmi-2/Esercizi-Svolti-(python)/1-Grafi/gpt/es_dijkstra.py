# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 09:30:26 2025

@author: 39324
"""

#scrivere l'algoritmo di dijkstra
from heapq import heappush, heappop

def dijkstra(G, s):
    n = len(G)
    padre = [-1]*n
    distanza = [float('inf')]*n
    
    padre[s] = s
    distanza[s] = 0
    H = []
    for v, costo in G[s]:
        heappush(H, (costo, s, v))
    
    while H:
        costo, u, v = heappop(H)
        if padre[v] == -1:
            padre[v] = u
            distanza[v] = costo
            for y, costoy in G[v]:
                if padre[y] == -1:
                    heappush(H, (distanza[v]+costoy, v, y))
    
    return distanza, padre


#Modifica l'algoritmo di Dijkstra per trovare il percorso più lungo in un grafo aciclico (DAG).

#Idea: basta utilizzare un maxheap invece che un minheap. Tuttavia python non ha un implementazione
#diretta dei maxheap, quindi bisogna usare un minheap cambiando i segni dei costi
def camminiMassimi(G, s):
    n = len(G)
    padre = [-1]*n
    distanza = [float('inf')]*n
    
    padre[s] = s
    distanza[s] = 0
    H = []
    for costo, v in G[s]:
        heappush(H, (-costo, s, v))
    
    while H:
        costo, u, v = heappop(H)
        if padre[v] == -1:
            distanza[v] = -costo
            padre[v] = u
            for y, costoy in G[v]:
                if padre[y] == -1:
                    nuovocosto = -(distanza[v]+costoy)
                    heappush(H, (nuovocosto, v, y))
    
    return distanza, padre