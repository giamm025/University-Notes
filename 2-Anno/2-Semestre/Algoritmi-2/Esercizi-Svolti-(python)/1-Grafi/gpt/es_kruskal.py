# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 17:27:50 2025

@author: 39324
"""

#%% STRUTTURA UNION e FIND
def Crea(G):
    return [(i, 1) for i in range(len(G))]
    #il primo ci dice il nome della compoennte il secondo il numero di nodi che ne fanno parte

def Find(C, u):
    while u != C[u]:
        u = C[u]
    return u
    #ogni componente ha come rappresentante il nodo radice (cioè il primo nodo che ne ha iniziato a far parte)
    #la Find risale quindi l'albero della componente e restituisce il "nome" del nodo radice

def Union(C, a, b):
    tota, totb = C[a][1], C[b][1]   #prendo il numero di nodi nella componente di A e il numero di nodi nella componente di B
    if tota >= totb:
        C[a] = (a, tota+totb)
        C[b] = (a, totb)
    else:
        C[a] = (b, tota)
        C[b] = (b, tota+totb)
        

#%% Dato un grafo pesato, connesso e non orientato e un numero massimo di archi che ogni nodo può avere:
#Modificare Kruskal in modo che l'albero generato rispetti la condizione che nessun nodo abbia più di un certo numero di connessioni.


def es(G, gradomax):
    n = len(G)
    
    T = [[] for _ in range(n)]
    
    E = [(costo, u, v) for u in range(n) for v, costo in G[u]]
    E.sort()

    C = Crea(G)  
    for costo, u, v in E:
        cu = Find(C, u)
        cv = Find(C, v)
        if cu != cv:
            gradoU = len(T[u])
            gradoV = len(T[v])
            if gradoU < gradomax and gradoV < gradomax:
                T[u].append(v)
                T[v].append(u)
                Union(C, u, v)
    
    return T

