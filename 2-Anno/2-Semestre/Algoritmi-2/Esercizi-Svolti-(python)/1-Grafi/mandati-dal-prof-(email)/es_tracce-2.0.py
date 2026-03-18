# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 10:35:00 2025

@author: 39324
"""
#%% dato un grafo non orientato rappresentato tramite liste di adiacenza, restituisca una lista di archi  
#in  numero minimo necessari per rendere il grafo  connesso. 

def es1(G):
    n = len(G)
    componente = vettComp(G)
    
    archi = []
    c = 2
    for i in range(n):
        if componente[i] == c:
            archi.append((0, i))
            G[0].append(i)
            G[i].append(0)
            c += 1
    
    return archi

def vettComp(G):
    n = len(G)
    componente = [-1]*n
    c = 1
    for i in range(n):
        if componente[i] == -1:
            DFS(G, i, c, componente)
            c += 1 
    
    return componente

def DFS(G, u, c, componente):
    componente[u] = c
    for v in G[u]:
        if componente[v] == -1:
            DFS(G, v, c, componente)
            
G = [[1, 4], [0, 4], [5, 7], [6], [0, 1], [2, 7], [3], [2, 5]]
print("Il vettore delle componenti è: ", vettComp(G))
print("Gli archi da aggiungere sono: ", es1(G))

#%% dato un DAG pesato G rappresentato mediante liste di adiacenza ed un suo vertice sorgente s, 
# restituisca il vettore delle distanze minime dei nodi da s.

def es2(G, s):
    n = len(G)
    sort = sortTop(G)
    distanza = [float('inf')]*n
    distanza[s] = 0
    for i in range(sort.index(s), len(sort)):
        u = sort[i]
        for v, costo in G[u]:
            distanza[v] = min(distanza[u]+costo, distanza[v])
    
    return distanza


def sortTop(G):
    n = len(G)
    gradoEnt = [0]*n
    for u in range(n):
        for i, c in G[u]:
            gradoEnt[i] += 1
            
    sorgenti = [x for x in range(n) if gradoEnt[x] == 0]
    
    sort = []
    while sorgenti:
        u = sorgenti.pop()
        sort.append(u)
        for i, c in G[u]:
            gradoEnt[i] -= 1
            if gradoEnt[i] == 0:
                sorgenti.append(i)
    
    return sort

G = [
    [(2, 1), (3, 2), (5, 4)],  # 0
    [(0, 5), (3, 1)],  # 1
    [],  # 2
    [(2, -3), (5, 6)],  # 3
    [(1, 6), (2, -2)],  # 4
    [],  # 5
    [],  # 6
]

print(es2(G, 0))
print(es2(G, 4))
print(es2(G, 6))


#%% labirinto di merda

#trasformiamo la matrice in un grafo in cui ogni nodo è una cella della matrice ed ogni arco a-->b 
#indica che si puo andare da a a b. Quindi ogni nodo avrà al massimo 4 archi, se tutte le celle adiacenti
#(sopra, sotto, destra e sinistra) sono impostate a 0 (e quindi attraversabili)

#per trasformare la matrice in un grafo utilizziamo il metodo classico in cui (i, j) diventa il nodo (i*n + j)

#una volta trasformata la matrice ci basterà trovare le porte ed effettuare una visita DFS. Alla fine restituiamo 
#il numero di 1 presenti nella lista visitati (cioè il numero di nodi, cioè celle, che abbiamo viistato)

def es3(M):
    
    G = trasforma(M)
    
    porte = trovaPorte(M)
    
    n = len(G)
    visitati = [0]*n
    for porta in porte:
        if visitati[porta] == 0:
            DFSm(G, porta, visitati)
    
    return sum(visitati)
    
    
    
def trasforma(M):
    n = len(M)
    G = [[] for _ in range(n*n)]
    for i in range(n):
        for j in range(n):
            u = nodo(i, j, n)
            
            if i-1 >= 0 and M[i-1][j]==0:
                G[u].append(nodo(i-1, j, n))
            
            if i+1<n  and M[i+1][j]==0:
                G[u].append(nodo(i+1, j, n))
                
            if j+1<n and M[i][j+1]==0:
                G[u].append(nodo(i, j+1, n))
                
            if j-1>=0 and M[i][j-1]==0:
                G[u].append(nodo(i, j-1, n))
    
    return G

def nodo(i, j, n):
    return i*n + j



def trovaPorte(M):
    n = len(M)
    porte = []
    for i in range(n):
        if M[i][0] == 0:
            porte.append(nodo(i, 0, n))
        
        if M[i][n-1] == 0:
            porte.append(nodo(i, n-1, n))
        
        if M[0][i] == 0:
            porte.append(nodo(0, i, n))
            
        if M[n-1][i] == 0:
            porte.append(nodo(n-1, i, n))
    
    return porte
            

def DFSm(G, u, visitati):
    visitati[u] = 1
    for i in G[u]:
        if visitati[i] == 0:
            DFSm(G, i, visitati)


M = [[1, 1, 0, 1, 1, 0, 1],
     [1, 0, 0, 0, 0, 0, 1],
     [1, 1, 0, 1, 1, 1, 1],
     [1, 1, 1, 0, 1, 0, 1],
     [0, 0, 1, 0, 1, 0, 1],
     [1, 0, 1, 1, 1, 0, 1],
     [1, 0, 1, 0, 1, 1, 1]]

print(es3(M))
