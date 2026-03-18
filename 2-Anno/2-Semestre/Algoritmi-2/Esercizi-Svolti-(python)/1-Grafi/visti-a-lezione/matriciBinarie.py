# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 09:49:14 2025

@author: 39324
"""

#%% DFS RICORSIVA
def DFS(G, u):
    n = len(G)
    visitati = [0]*n
    DFSr(G, u, visitati)
    return [x for x in range(n) if visitati[x]==1]

def DFSr(G, u, visitati):
    visitati[u]=1 
    for i in range(len(G)):
        if G[u][i] and visitati[i]==0:
            DFSr(G, i, visitati)


# DFS ITERATIVA
def DFSi(G, u):
    n = len(G)
    visitati = [0]*n
    pila = [u]
    while pila:
        u = pila.pop()
        visitati[u] = 1
        for i in range(n):
            if G[u][i] and visitati[i]==0:
                visitati[i] = 1
                pila.append(i)
                
    return [x for x in range(n) if visitati[x]==1]


#%% VETTORE DEI PADRI RICORSIVO
def vettPadri(G, u):
    n = len(G)
    padre = [-1]*n
    vettPadri2(G, u, u, padre)
    return padre

def vettPadri2(G, u, p, padre):
    padre[u]=p 
    for i in range(len(G)):
        if G[u][i] and padre[i]==-1:
            vettPadri2(G, i, u, padre)    

#VETTORE DEI PADRI ITERATIVO
def vettPadriI(G, u):
    n = len(G)
    padre = [-1]*n
    padre[u]=u
    
    pila = [u]
    while pila:
        u = pila.pop()
        for i in range(n):
            if G[u][i] and padre[i]==-1:
                padre[i]=u
                pila.append(i)
    return padre


#%% TROVARE I POZZI NORMALI
def findPozzi(G):
    n = len(G)
    pozzi = []
    for u in range(n):
        count = G[u].count(1)
        if count == 0:
            pozzi.append(u)
    return pozzi
    

#prove
G =[[0, 1, 0, 0],
    [0, 0, 1, 0],
    [1, 0, 0, 1],
    [0, 0, 0, 0]]

#print("I pozzi sono: ", findPozzi(G))
print("La DFS iterativa da 0 ritorna: ", DFS(G, 0))
print("La DFS iterativa da 2 ritorna: ", DFSi(G, 2))
print("Il vettore dei padri DFS partendo da 0 è: ", vettPadri(G, 0))
print("Il vettore dei padri DFS partendo da 0 è: ", vettPadriI(G, 0))