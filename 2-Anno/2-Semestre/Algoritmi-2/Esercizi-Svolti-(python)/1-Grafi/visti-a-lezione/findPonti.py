# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 10:44:30 2025

@author: 39324
"""

def findPonti(G):
    n = len(G)
    ponti = []
    visitati = [0]*n
    livello = [float('inf')]*n
    DFS(G, 0, 0, 0, livello, ponti, visitati)
    return ponti

def DFS(G, u, p, lv, livello, ponti, visitati):
    visitati[u] = 1
    livello[u] = lv
    b = lv
    for i in G[u]:  

        if visitati[i] == 0:
            sotto = DFS(G, i, u, lv+1, livello, ponti, visitati)    #il minimo lv che i miei figli riescono a raggiungere
            if sotto > livello[u]:                                  #se riescono a raggiungere solo nodi SOTTO di me
                ponti.append((u, i))                                #allora quest'arco è un ponte
            
            b = min(sotto, b)                 #se invece riescono a raggiungere qualcuno sopra di me anche io potro raggiungerlo
                                              #questo è il minimo livello che riesco a raggiungere, anche indirettamente (cioe
                                              #passando per i miei figli)  
        if i!=p and livello[i] < b:
            b = livello[i]                    #questo è il minimo livello che riesco a raggiungere direttamente      
            
    return b

G = [[3, 4, 5, 8], [2, 7], [1, 6, 7], [0, 4, 7], [0, 3], [0, 8], [2], [1, 2, 3], [0, 5]]
print(findPonti(G))


