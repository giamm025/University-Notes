# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 12:48:17 2025

@author: 39324
"""

#%% VISITA BFS DI UN GRAFO DIRETTO
def BFS(G, u):
    n = len(G)
    visitati = [0]*n
    visitati[u] = 1
    
    coda = [u]
    i = 0
    while i<len(coda):
        u = coda[i]
        i += 1
        for v in G[u]:
            if visitati[v]==0:
                visitati[v]=1
                coda.append(v)

            
    return [x for x in range(n) if visitati[x]==1]

G=[  [1,5], [2], [3], [4], [ ], [2,4], [2]]
print("I nodi visitati sono: ", BFS(G, 0))

#%% OTTENERE L'ALBERO BFS memorizzato come vettore dei padri
def vettPadri(G, u):
    n = len(G)
    padre = [-1]*n
    padre[u] = u
    
    coda = [u]
    i = 0
    while i<len(coda):
        u = coda[i]
        i += 1
        for v in G[u]:
            if padre[v]==-1:
                padre[v]=u
                coda.append(v)
                
    return padre

G=[  [1,5], [2], [3], [4], [ ], [2,4], [2]]
print("Il vettore dei padri è: ", vettPadri(G, 0))


#%% OTTENERE IL VETTORE DELLE DISTANZE DI UN GRAFO DIRETTO
def vettDistanze(G, u):
    n = len(G)
    distanza = [-1]*n
    distanza[u] = 0
    
    coda = [u]
    i = 0
    while i<len(coda):
        u = coda[i]
        i += 1
        for v in G[u]:
            if distanza[v]==-1:
                distanza[v]=distanza[u]+1
                coda.append(v)

            
    return distanza

G=[  [1,5], [2], [3], [4], [ ], [2,4], [2]]
print("Il vettore delle distanze è: ", vettDistanze(G, 0))

#%% DATI I NODI a E b TROVARE LE SFERE DI INFLUENZA. {esonero 2024}.
def vettDistanze(G, u):
    n = len(G)
    distanza = [-1]*n
    distanza[u] = 0
    coda = [u]
    i = 0
    while i < len(coda):
        u = coda[i]
        i += 1
        for v in G[u]:
            if distanza[v] == -1:
                distanza[v] = distanza[u]+1
                coda.append(v)
        
    
    return distanza

def trasponi(G):
    n = len(G)
    GT = [[] for _ in range(n)]
    for u in range(n):
        for i in G[u]:
            GT[i].append(u)
    return GT


def findSfereInfluenza(G, a, b):
    n = len(G)
    sfera = [-1]*n
    
    GT = trasponi(G)            #traspongo perche dobbiamo trovare le distanze da x->a e da x->b
    distA = vettDistanze(GT, a)
    distB = vettDistanze(GT, b)

    for i in range(n):
        if distA[i] < distB[i]:
            sfera[i] = a
            
        elif distB[i] < distA[i]:
            sfera[i] = b
        
        #se è equidistante lascio -1
    
    return sfera


G = [[1, 2, 10], [4, 5, 9], [7], [0, 4, 9], [9], [2, 6, 8], [4, 7], [5], [0, 2], [6], [9]]
print("Le sfere di Influenza sono: ", findSfereInfluenza(G, 6, 2))


      


