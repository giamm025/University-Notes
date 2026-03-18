# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 18:09:47 2025

@author: 39324
"""

def kruskal(G):
    n = len(G)
    T = [[] for _ in range(n)]      #l'albero inizialmente ha tutti i nodi ma senza arch
    
    E = []                          #inizializziamo la lista E con tutti gli archi
    for u in range(n):
        for v, costo in G[u]:
            E .append(costo, u, v)
    E.sort()                        #ordiniamo la lista (crescente)
    
    C = Crea(G)                     #ci creiamo la UNION e FIND del grafo
    for costo, u, v in E:           #per ogni arco del grafo
        cu = Find(C, u)             #vediamo la componente di u
        cv = Find(C, v)             #e la componente di v
        if cu != cv:                #Se sono nella stessa componente questo arco creerebbe un ciclo
            T[u].append(v)          #Se sono in due componenti diversa inseriamo l'arco
            T[v].append(u)
            Union(C, u, v)
    
    return T



#STRUTTURA UNION e FIND
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