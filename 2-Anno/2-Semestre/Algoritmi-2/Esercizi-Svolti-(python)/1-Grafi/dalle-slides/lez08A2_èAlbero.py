# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 09:56:07 2025

@author: 39324
"""

#%% dato un grafo G non diretto e connesso e due suoi nodi u e v, trova i nodi che hanno la stessa distanza da u e v.
def equidistanti(G, u, v):
    n = len(G)
    A = vettDistanze(G, u)
    B = vettDistanze(G, v)
    
    equidistanti = []
    for i in range(n):
        if A[i]==B[i]:
            equidistanti.append(i)
    
    return equidistanti

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

G = [[1], [0, 2, 6], [1], [6, 4, 5], [3], [3], [1, 3]]
print(equidistanti(G, 0, 5))

#%% VERFICARE CHE G SIA UN ALBERO

#un albero è un grafo connesso aciclico. Possiamo quindi effettuare una visita DFS e verificare se sono presenti cicli.
#nel caso in cui troviamo cicli chiaramente NON è un albero. Se invece NON ci sono cicli dobbiamo controllare che il grafo
#sia connesso. Per fare ciò basta vedere se ci sono nodi non visitati.

#TUTTAVIA, nel caso di grafi diretti devo stare attento al nodo da cui inizio la visita. Se lo scelgo a caso rischio di partire
#, ad esempio, da un nodo pozzo. In questo caso, anche se il grafo fosse connesso, la lista visitati conterrebbe tutti 0, poiche
#il pozzo non ha archi uscenti. Scegliamo quindi una sorgente da cui far partire la visita.
def èAlbero(G):
    
    if èDiretto(G):
        #se il grafo è diretto dobbiamo innanzitutto trovare il nodo sorgente da cui iniziare la visita
        sorgenti = trovaSorgenti(G)
        if len(sorgenti) != 1: return False, "il grafo ha piu di una sorgente"     #se ho piu di una sorgente NON puo essere un albero
        s = sorgenti[0]
   
    else:
        #se il grafo è indiretto posso partire da un nodo qualsiasi
        s = 0
        
    #Faccio la visita e nel mentre verifico se ci sono cicli
    n = len(G)
    visitati = [0]*n
    aciclico = DFS(G, s, visitati)
    
    #Controllo: Se ho raggiunto tutti i nodi il grafo è connesso
    raggiunti = [x for x in range(n) if visitati[x]==2]
    connesso = len(raggiunti) == n
    
    return aciclico and connesso
    
def èDiretto(G):
    n = len(G)
    padre = [-1]*n
    padre[0] = 0
    for u in range(n):
        for i in G[u]:
            padre[i] = u
    
    count = 0
    for u in range(1, n):
        for i in G[u]:
            if i == padre[u]:
                count += 1
    
    return count != n-1           #se ogni nodo (tranne la radice) ha un arco verso suo padre è un grafo INDIRETTO
    
def trovaSorgenti(G):
    n = len(G)
    gradoEnt = [0]*n
    for u in range(n):
        for i in G[u]:
            gradoEnt[i] += 1
    
    return [x for x in range(n) if gradoEnt[x] == 0]
    
    
def DFS(G, u, visitati):
    visitati[u] = 1
    for i in G[u]:
        if visitati[i] == 1:
            return False
        
        if visitati[i] == 0:
            if not DFS(G, i, visitati):     #se sotto di me NON è aciclico 
                return False
    
    visitati[u] = 2
    return True
    

GI = [[1, 2], [0], [0]]
GD = [[1], [2], []]
print(èAlbero(GI))
print(èAlbero(GD))

