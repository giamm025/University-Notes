# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 09:20:34 2025

@author: 39324
"""
'''Devo eseguire n lavori, ognuno dei quali ha un tempo d’esecuzione specifico. Mi 
 è fornito un vettore T di n componenti, dove T[i] rappresenta il tempo richiesto per eseguire il lavoro i. Inoltre ho la lista di liste P di n componenti, dove P[i] contiene i lavori che devono essere completati prima che io possa iniziare il lavoro i.

Progettare un algoritmo che, dati T e P, in tempo O(n^2) calcoli il tempo minimo necessario per completare tutti i lavori tenendo conto che è possibile eseguire più lavori in parallelo.

L'algoritmo deve restituire float('inf') nel caso in cui non sia possibile completare tutti i lavori (ad esempio a causa di cicli di dipendenza tra i lavori).
'''

def es(P, T):
    PT = trasponi(P)
    
    sort = sortTop(PT)
    print(sort)
    if len(sort)!=len(T): return float('inf')
    
    s = sort[0]
    tot = DFSt(PT, T, s)
    return tot 

def DFSt(P, T, u):
    mas = 0
    for i in P[u]:
        costoFiglio = DFSt(P, T, i)
        if costoFiglio > mas:
            mas = costoFiglio
    
    return  T[u] + mas


def trasponi(G):
    n = len(G)
    GT = [[] for _ in range(n)]
    for u in range(n):
        for i in G[u]:
            GT[i].append(u)
    
    return GT

def sortTop(P):
    n = len(P)
    gradoEnt = [0]*n
    for u in range(n):
        for i in P[u]:
            gradoEnt[i] += 1
    
    sort = []
    sorgenti = [x for x in range(n) if gradoEnt[x] == 0]
    while sorgenti:
        u = sorgenti.pop()
        sort.append(u)
        for i in P[u]:
            gradoEnt[i] -= 1
            if gradoEnt[i] == 0:
                sorgenti.append(i)
    
    return sort

T = [3, 2, 5, 4, 3, 1, 9, 8]
P = [[1, 2], [3], [3], [4], [5], [], [0], [2]]
print("Il costo minimo è: ", es(P, T))