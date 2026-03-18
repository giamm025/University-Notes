# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 21:38:29 2025

@author: 39324
"""

def es1(n):
    
    G = crea(n)
    
    #lo aggiungo per completezza. Ma in reata, siccome da ogni nodo u eseguiamo solo operazioni
    #che ne aumentano il valore (+1, *2, *3) avremo gia che ogni nodo punta solo ad altri piu
    #grandi di lui => gli archi di G sono gia tutti da sinistra verso destra => è gia un sortTop
    sort = sortTop(G)
    
    percorsi = [0]*(n+1)
    percorsi[2] = 1
    for u in range(2, n+1):
      for i in G[u]:
          percorsi[i] += percorsi[u]
    
    print(percorsi)
    return percorsi[n]
    
    
    
def crea(n):
    #per comodità inserisco anche i nodi 0 e 1 che pero NON avranno archi.
    #mi servono solo perche cosi posso avere G[10] per vedere gli adiacenti di 10
    #e G[2] per vedere gli adiacenti di 2
    G = [[] for _ in range(n+1)]
    
    #inserisco gli archi. In particolare controllo che il risultato sia < n
    #per evitare di far crescere troppo il numero di nodi del grafo (e perche
    #ho inizializzato il grafo con nodi che arrivano fino ad n. Quindi accedere
    #a G[n+1] darebbe out of range)
    for i in range(2, n):
        if i+1 <= n:
            G[i].append(i+1)
            
        if i*2 <= n:
            G[i].append(i*2)
            
        if i*3 <= n:
            G[i].append(i*3)
    
    return G

def sortTop(G):
    n = len(G)
    gradoEnt = [0]*n
    for u in range(n):
        for i in G[u]:
            gradoEnt[i] += 1
    
    sorgenti = [x for x in range(n) if gradoEnt[x] == 0]
    
    sort = []
    while sorgenti:
        u = sorgenti.pop()
        sort.append(u)
        for i in G[u]:
            gradoEnt[i] -= 1
            if gradoEnt[i] == 0:
                sorgenti.append(i)
    

    if len(sort) != len(G): return None
    return sort


print(es1(10))