# -*- coding: utf-8 -*-
"""
Created on Tue May 13 10:01:01 2025

@author: 39324
"""

def es6(G):
    n = len(G)
    C = [-1]*n                  #Nessun nodo è colorato all'inizio
    for u in range(n):          #serve a gestire il caso in cui il grafo fosse sconnesso
        if C[u] == -1:          #se ancora non l'ho colorato
            colora(G, C, u)

def colora(G, C, u):
    coda = [u]
    i = 0
    while i<len(coda):
        u = coda[i]
        rossi = 0                   #per ogni nodo resetto il contatore dei rossi
        neri = 0                    #e il contatore dei neri
        for v in G[u]:              #per ogni vicino v di u

            if C[v] == "Rosso":     #se è rosso incremento il contatore dei rossi
                rossi += 1
            elif C[v] == "Nero":    #se è nero incremento il contatore dei neri
                neri += 1
            else:
                coda.append(v)      #se non ha ancora un colore devo andare a colorarlo
            
        C[u] = "Rosso" if rossi < neri else "Nero"
        i += 1

#La complessita dovrebbe comunque essere O(n+m) perche il for iniziale itera solo sui nodi non colorati
#questo significa che se il nodo è connesso itererà una sola volta colorando tutti i nodi insieme
#se il grafo è sconnesso itera una volta  per ogni componente connessa.
#In generale l'idea è che a fine algoritmo avremo colorato tutti i nodi una sola volta.