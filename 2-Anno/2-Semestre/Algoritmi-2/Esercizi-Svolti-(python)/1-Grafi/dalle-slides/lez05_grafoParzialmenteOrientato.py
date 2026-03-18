# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 09:36:03 2025

@author: 39324
"""

# DATO UN GRAFO PARZIALMENTE ORIENTATO DECIDE COME ORIENTARE GLI ARCHI PER NON AVERE CICLI

#sfruttando il fatto che "un grafo ha un sort topologico <=> è un DAG" produco il sort topologico del grafo basandomi SOLO SUGLI
#ARCHI DIRETTI. Scorro poi gli archi indiretti e li orientero in modo da mantenere il sort topologico (cioè tutti da sinistra
#verso destra). In questo modo garantisco che venga fuori un DAG.

def orienta(G):
    n = len(G)
    sort = sortTop(G)
    
    F = [[] for _ in range(n)]
    visitati = [0]*n
    for u in sort:
        visitati[u] = 1
        for i in G[u][0]:
            F[u].append(i)          #gli archi diretti li copio cosi come sono
    
        for v in G[u][1]:
            if visitati[v] == 0:    #se l'ho gia visitato significa che si trova prima di me nel sort topologico
                F[u].append(v)      #e NON posso avere un arco all'indietro (da destra a sinistra) perche creerebbe ciclo

    return F    

def sortTop(G):
    n = len(G)
    gradoEnt = [0]*n
    for u in range(n):
        for i in G[u][0]:
            gradoEnt[i] += 1
    
    sorgenti = [x for x in range(n) if gradoEnt[x] == 0]
    
    sort = []
    while sorgenti:
        s = sorgenti.pop()
        sort.append(s)
        for i in G[s][0]:
            gradoEnt[i] -= 1
            if gradoEnt[i] == 0:
                sorgenti.append(i)
    
    if len(sort) != len(G): return None     #significa che c'è un ciclo e non posso fare il sort
    return sort

G = [([], [2,3]),
     ([0,3], [2]),
     ([],[0,1,4]),
     ([2],[0]),
     ([],[2])]

print(orienta(G))