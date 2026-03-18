# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 09:08:14 2025

@author: 39324
"""
from heapq import heappush, heappop 

#%% RESTITUIRE I NODI IRAAGIUNGIBILI SENZA PASSARE PER UN NODO PERICOLOSO

# Faccio una semplice visita BFS al grafo a partire da s. Quando incontro un nodo pericoloso NON lo visito
# Alla fine tutti i nodi NON pericolosi NON visitati saranno irraggiungibili
def irraggiungibili(G, s, P):
    if P[s] == 1: return []
    
    n = len(G)
    visitati = [0]*n
    coda = [s]
    i = 0
    while i < len(coda):
        u = coda[i]
        i += 1
        for v in G[u]:
            if visitati[v] == 0 and P[v]==0:
                visitati[u] = 1
                coda.append(v)
                
            
    return [x for x in range(n) if visitati[x] == 0 and P[x] == 0]

G = [[1, 2], [0, 3], [0, 3], [1, 2, 4], [3]]
P = [0, 1, 0, 0, 0] 
print(irraggiungibili(G, 0, P)) 

#%% CAMMINO CHE ATTRAVERSA IL MINOR NUMERO DI NODI PERICOLOSI

#Possiamo modelare il probelma come un grafo pesato, in cui ogni arco costa 0 se il nodo raggiungo è NON pericoloso
#oppure 1 se è pericoloso. In questo modo applicando una modifica all'algoritmo di Dijkstra riusciamo a risolvere il problema

def cammino(G, s, P):
    n = len(G)
    costo = [float('inf')]*n  #come in Dijkstra questo lo uso per salvare il costo di ogni nodo
    padre = [-1]*n              #qui restituiro l'albero dei cammini memorizzato come vett dei padri
    padre[s] = s
    costo[s] = P[s]
    
    H = []                      #questo sarà il nostro heap
    for y in G[s]:
        heappush(H, (P[y], s, y))
    
    while H:
        peso, s, y = heappop(H)
        if padre[y]==-1:
            padre[y] = s
            costo[y] = peso
            for v in G[y]:
                heappush(H, (costo[y]+P[v], y, v))
    
    return padre


G = [[1, 2], [0, 3], [0, 3], [1, 2, 4], [3]]
P = [0, 1, 0, 1, 0]  # I nodi 1 e 3 sono pericolosi
print(cammino(G, 0, P))

#%% TROVARE I CAMMINI SUPER MINIMI

#Quanto facciamo heappush di un arco oltre a passare il costo di quel cammino passiamo come secondo criterio di ordinamento
#il numero di archi attraversati fino ad ora. In questo modo, tra due cammini con lo stesso costo, verra estratto quello che
#attraversa il minor numero di nodi/archi => il cammino superminimo
def camminiSuperMinimi(G, s):
    n = len(G)
    padre = [-1]*n
    distanza = [-1]*n
    costo = [float('inf')]*n
    costo[s] = 0
    distanza[s] = 0
    padre[s] = s
    
    H = []  #il nostro Heap
    for v, costov in G[s]:
        heappush(H, (costov, 0, s, v))       #fino ad ora ho attraversato 0 archi
        
    while H:
        costoy, num_archi, s, y = heappop(H)
        if padre[y] == -1:
            padre[y] = s
            distanza[y] = distanza[s]+1     #ogni nodo attraversa gli stessi archi di suo padre + 1 (che è quello che lo ha portato da me)
            costo[y] = costoy               #per ogni nodo mi salvo il cosrto che ho dovuto spendere per raggiungerlo (opzionale, non è richiesto)
            for v, costov in G[y]:
                nuovocosto = costoy+costov  #il costo di questo arco è dato dal costo speso fino a qui + il costo del singolo arco da attraversare
                heappush(H, (nuovocosto, distanza[y], y, v))   
    
    return padre, costo, distanza

G = [[(1, 2), (4, 5)], [(0, 2), (2, 3)], [(1, 3), (3, 3)], [(2, 3), (4, 3)], [(0, 5), (3, 3)]]
print(camminiSuperMinimi(G, 0))

#%% TROVARE IL CAMMINO MASSIMO CHE COLLEGA I NODI a E b

#Possiamo pensare che ogni arco pesi 1 ed applicare l'algoritmo di Dijkstra con un maxheap
#piuttosto che un minheap. Tuttavia in pyton esiste solo il minheap (cosi dice gpt) e quindi
#per ottenere il maxheap bisogna invertire il segno di ciascun costo.
def findCiclo(G):
    n = len(G)
    visitati = [0]*n
    return DFS(G, 0, visitati)

def DFS(G, u, visitati):
    visitati[u] = 1
    for i in G[u]:
        if visitati[i] == 1:
            return True
        
        if visitati[i] == 0:
            if DFS(G, i, visitati):
                return True
    
    visitati[u] = 2
    return False

def percorsoMassimo(G, a, b):
    n = len(G)
    distanza = [1]*n
    padre = [-1]*n
    distanza[a] = 0
    padre[a] = a
    
    if findCiclo(G): return float('inf')
    
    H = []                          #il nostro min heap. TUTTAVIA in questo caso ho bisogno di un max heap, quindi
    for i in G[a]:
        heappush(H, (-1, a, i))     #gpt suggerisce di invertire il segno di tutti i costi.
        
    while H:
        d, x, y = heappop(H)
        if distanza[y] == 1:
            padre[y] = x
            distanza[y] = -d
            for v in G[y]:
                heappush(H, (-(distanza[y]+1), y, v))
    
    return distanza[b], padre

G = [[1, 2], [], [3, 4], [4], [1]]
print(percorsoMassimo(G, 0, 1))