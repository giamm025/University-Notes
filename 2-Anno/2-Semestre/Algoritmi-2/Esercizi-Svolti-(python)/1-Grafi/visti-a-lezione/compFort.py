# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 08:34:51 2025

@author: 39324
"""

#RESTITUISCE LA LISTA DEI NODI NELLA STESA COMPONENTE CONNESSA DI u
def compFort(G, u):
    n = len(G)
    GT = trasponi(G)    #permette di capire quali nodi raggiungono u 
    A = [0]*n           #visitati per la visita a G
    B = [0]*n           #visitati per la visita a GT
    
    DFS(G, u, A)        #alla fine A[v]==1 se v è raggiungibile da u
    DFS(GT, u, B)       #alla fine B[v]==1 se u è raggiungibile da v
    
    comp = []
    for i in range(n):
        if A[i] and B[i]:   #l'intersezione tra A e B (cioè i nodi raggiungibili e che 
            comp.append(i)  #raggiungono u) fanno parte della sua stessa componente
    
    return comp

def DFS(G, u, visitati):
    visitati[u] = 1
    for v in G[u]:
        if visitati[v]==0:
            DFS(G, v, visitati)


def trasponi(G):
    n = len(G)
    GT = [[] for _ in range(n)]
    for u in range(n):
        for i in G[u]:
            GT[i].append(u)
    
    return GT

G = [[], [2], [3], [1]]
print(compFort(G, 1))

