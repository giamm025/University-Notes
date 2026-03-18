# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 09:04:34 2025

@author: 39324
"""

#%% TROVARE I NODI ARTICOLAZIONE DI UN GRAFO

#Credo che i punti di articolazione siano tutti quei nodi coinvolti in un arco ponte TRANNE le foglie.
#Se infatti andiamo a rimuovere una foglia il grafo avrà un nodo in meno, ma resterà connesso
def articolazioni(G):
    n = len(G)
    articolazioni = []
    ponti = findPonti(G)
    for u, v in ponti:
        if len(G[u]) != 1:              #se u non è una foglia
            articolazioni.append(u)
            
        if len(G[v]) != 1:              #se v non è una foglia
            articolazioni.append(v)
    
    return articolazioni


def findPonti(G):
    n = len(G)
    ponti = []
    livello = [float('inf')]*n
    DFS(G, 0, 0, 0, livello, ponti)
    return ponti

def DFS(G, u, p, lv, livello, ponti):
    livello[u] = lv
    min_raggiungibile = lv
    for i in G[u]:
        
        if livello[i] == float('inf'):                      #ancora non l'ho visitato
            sotto = DFS(G, i, u, lv+1, livello, ponti)
            if sotto > livello[u]:                          #se i miei discendenti raggiungono solo livelli maggiori (cioè sotto) di me => è un ponte
                ponti.append((u, i))
            
            min_raggiungibile = min(sotto, min_raggiungibile)
        
        if i!=p and livello[i] < min_raggiungibile:         #se riesco a raggiungere un nodo di livello minore (cioe sopra) di me DIVERSO da mio padre
            min_raggiungibile = livello[i]                  #questo diventa il nuovo livello minimo (cioè piu alto) che riesco a raggiungere
    
    return min_raggiungibile

G = [[3, 4, 5, 8], [2, 7], [1, 6, 7], [0, 4, 7], [0, 3], [0, 8], [2], [1, 2, 3], [0, 5]]
print(articolazioni(G))

#%% DIRE SE G è UN GRAFO CACTUS

#Applichiamo una modifca all'algoritmo di Tarjian. L'idea è che se piu di uno dei miei figli riesce a raggiungere
#un mio antenato, allora io e alcuni dei miei archi siamo parte di piu di un ciclo. QUindi mi trovo in un grafo cactus.
#il grafo dato in input si assume come gia NON orienttao e CONNESSO (quindi non va controllato)

def cactus(G):
    n = len(G)
    figli = [0]*n   #tiene il conto di quanti figli raggiungono un nodo sopra di me
    livello = [float('inf')]*n
    DFSc(G, 0, 0, 0, livello, figli)
    
    for u in range(n):
        if figli[u] > 1:
            return False
        
    return True

def DFSc(G, u, p, lv, livello, figli):
    livello[u] = lv
    min_raggiungibile = lv
    for i in G[u]:
        if livello[i] == float('inf'):  #ancora non l'ho visitato
            b = DFSc(G, i, u, lv+1, livello, figli)
            if b < livello[u]:
                figli[u] += 1
                
            min_raggiungibile = min(min_raggiungibile, b)
            
        if i!=p:
            min_raggiungibile = min(min_raggiungibile, livello[i])
        
    return min_raggiungibile


G = [[1, 4], [0, 2], [1, 3, 4], [1, 2], [0, 2]]
print(cactus(G))

G = [[1, 4, 6], [0, 2], [1, 3, 4, 5], [2, 5], [0, 2], [2, 3], [0]]
print(cactus(G))