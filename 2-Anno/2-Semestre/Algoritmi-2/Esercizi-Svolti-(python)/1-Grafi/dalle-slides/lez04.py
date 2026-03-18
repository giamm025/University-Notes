# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 08:36:48 2025

@author: 39324
"""

#%% DATO UN ALBERO MEMORIZZATO COME VETTORE DEI PADRI P RESTITUIRE LA DISTANZA TRA u E v NELL'ALBERO

#Scorro il vettore dei padri e mi costruisco un grafo (l'albero) equivalente
#dopodichè calcolo il vett delle distanze con la BFS a partire da u e restituisco
#distanza[v] (che rappresenta proprio la distanza tra u e v)
def distanza(P, u, v):
    n = len(P)
    G = [[] for _ in range(n)]
    for i in range(n):
        p = P[i]
        if i != p:
            G[p].append(i)
            G[i].append(p)

    distanza = vettDistanze(G, u)
    return distanza[v]


def vettDistanze(G, u):
    n = len(G)
    distanza = [-1]*n
    distanza[u] = 0
    coda = [u]
    i = 0
    while i<len(coda):
        u = coda[i]
        i+=1
        for v in G[u]:
            if distanza[v]==-1:
                distanza[v] = distanza[u] + 1
                coda.append(v)
    
    return distanza
            


P = [0, 2, 2, 1, 2, 5, 3, 3, 9, 1]
print(distanza(P, 3, 6))


#%% DATO UN ALBERO MEMORIZZATO COME VETT DEI PADRI RESTITUIRE LA LISTA DEI DISCENDETI DI x
def discendenti(padre, x):
    n = len(padre)
    G = [[] for _ in range(n)]
    for u in range(n):
        p = padre[u]
        G[p].append(u)
        #in questo modo costruisco un grafo che ha solo archi padre-->figlio
        #e che quindi si puo esplorare solo verso il basso senza risalire
    
    sottoalbero = [x]
    DFSb(G, x, sottoalbero)
    return sottoalbero

def DFSb(G, x, sottoalbero):
    #non metto controlli con visitati perche tanto gli alberi sono aciclici. 
    #Mi fermero quando G[x] è vuoto, cioè quando arrivo a una foglia
    for i in G[x]:
        if i != x:          
        #altrimenti la radice che ha come padre se stessa
        #va in ricorsione infinita
            sottoalbero.append(i)
            DFSb(G, i, x, sottoalbero)
    
padre = [2, 3, 2, 4, 2, 3, 4, 0]
print(discendenti(padre, 4))
print(discendenti(padre, 2))


#%% DATO G TROVARE IL GRAFO DELLE PARTI