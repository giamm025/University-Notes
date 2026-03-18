# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 09:52:02 2025

@author: 39324
"""

#%% UNIRE LE COMPONENTI DI UN GRAFO INDIRETTO
def vettComp(G):
    n = len(G)
    comp = [-1]*n
    i = 1
    for u in range(n):
        if comp[u]==-1:
            DFSc(G, u, comp, i)
            i += 1
    
    return comp

def DFSc(G, u, comp, i):
    comp[u]=i
    for v in G[u]:
        if comp[v]==-1:
            DFSc(G, v, comp, i)

def es1(G):
    comp = vettComp(G)
    lista = []
    i = 2
    for u in range(len(G)):
        if comp[u] == i:
            lista.append((0, u))
            i += 1
    return lista

G = [[1, 4], [0, 4], [5, 7], [6], [0, 1], [2, 7], [3], [2, 5]]
print("Il vettore delle componenti è: ", vettComp(G))
print("Gli archi da aggiungere sono: ", es1(G))
