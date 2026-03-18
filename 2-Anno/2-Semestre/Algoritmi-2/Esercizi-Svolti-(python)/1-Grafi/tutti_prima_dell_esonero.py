# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 10:58:18 2025

@author: 39324
"""

#%% Nodi raggiungibili da u con una DFS in un grafo memroizzato con matrice di adiacenza
def raggiungibiliM(M, u):
    n = len(M)
    visitati = [0]*n
    DFSm(M, u, visitati)
    return [x for x in range(n) if visitati[x] == 1]

def DFSm(M, u, visitati):
    n = len(M)
    visitati[u] = 1
    for i in range(n):
        if M[u][i] and visitati[i]==0:
            DFSm(M, i, visitati)

#%% Nodi raggiungibili da u con una DFS classica con liste di adiacenza
def raggiungibili(G, u):
    n = len(G)
    visitati = [0]*n
    DFSr(G, u, visitati)
    return [x for x in range(n) if visitati[x] == 1]

def DFSr(G, u, visitati):
    visitati[u] = 1
    for i in G[u]:
        if visitati[i] == 0:
            DFSr(G, i, visitati)
            
#%% DFS Iterativa

def raggiungibiliI(G, u):
    n = len(G)
    visitati = [0]*n
    DFSi(G, u, visitati)
    return [x for x in range(n) if visitati[x] == 1]

def DFSi(G, u, visitati):
    n = len(G)
    stack = [u]
    while stack:
        u = stack.pop()
        visitati[u] = 1
        for i in G[u]:
            if visitati[i] == 0:
                stack.append(i)
    
    return [x for x in range(n) if visitati[x] == 1]

def trasforma(G):
    n = len(G)
    M = [[0 for _ in range(n)] for _ in range(n)]
    for u in range(n):
        for i in G[u]:
            M[u][i] = 1
    
    return M


G = [[1], [2], [0, 3], []]

M = trasforma(G)

print(raggiungibiliM(M, 0))
print(raggiungibili(G, 0))
print(raggiungibiliI(G, 0))
#%%

#IDEA: Faccio partire una visita BFS in contemporanea da tutti i nodi rossi
#mi fermo appena trovo un nodo x verde (cioe tc. verde[x] == 1)
def es9(G, v1, v2):
    
    if v1.intersection(v2) != set(): return 0       #se l'intersezione NON è vuota ritorna 0
    
    n = len(G)
    verde = [0]*n
    for u in v2:
        verde[u] = 1
    
    #Inizializzo la BFS
    distanza = [float('inf')]*n
    padre = [-1]*n
    coda = []
    for u in v1:
        distanza[u] = 0     #poiche faccio partire le visite dai nodi rossi ciascuno di questi ha distanza 0 
        padre[u] = u        #e sono tutti radice della propria visita BFS
        coda.append(u)
    
    i = 0
    while i < len(coda):
        u = coda[i]
        i += 1 
        for v in G[u]:
            if distanza[v] == float('inf'):
                distanza[v] = distanza[u]+1
                coda.append(v)
                
                if verde[v] == 1:
                    return distanza[v]
        

#%%

def DFSPadri(G, u):
    n = len(G)
    padre = [-1]*n
    DFSp(G, u, u, padre)
    return padre

def DFSp(G, u, p, padre):
    padre[u] = p
    for i in G[u]:
        if padre[i] == -1:
            DFSp(G, i, u, padre)

#%% 
    
def cammino(G, a, b):
    padre = DFSPadri(G, a)
    
    if padre[b] == -1: return []    #b non ha padre <=> non è raggiungibile da a
    
    cammino = []
    u = b
    while u != padre[u]:            #risalgo l'albero fino alla radice
        cammino.append(u)           #e mi segno i nodi che attraverso
        u = padre[u]
    
    cammino.append(a)           
    cammino.reverse()       #in questo modo abbiamo trova il cammino b->a. Per avere da a->b faccio reverse()
    return cammino

#%%

def bicolora(G):
    n = len(G)
    colore = [-1]*n
    DFSc(G, 0, 0, colore)   #faccio una DFS e colore tutti i nodi che incontro.
    
    visitati = [0]*n
    if èBicolorabile(G, 0, colore, visitati):       return colore
    else:                                           return "Impossibile Bi-Colorare! G contiene un cico dispari"

def DFSc(G, u, c, colore):
    colore[u] = c
    for i in G[u]:
        if colore[i] == -1:
            DFSc(G, i, 1-c, colore)

def èBicolorabile(G, u, colore, visitati):
    visitati[u] = 1
    for i in G[u]:
        
        if colore[i] == colore[u]:
            return False
        
        if visitati[i] == 0:
            if not èBicolorabile(G, i, colore, visitati):
                return False
    
    return True

G = [[1], [2], [3], [0]]    #ciclo parti 0-1-2-3-0
print(bicolora(G))

G = [[1], [2], [0]]         #ciclo dispari 0-1-2-0
print(bicolora(G))

#%%

def componenti(G):
    n = len(G)
    comp = [-1]*n
    c = 0
    for u in range(n):
        if comp[u] == -1:
            DFSComp(G, u, c, comp)
            c += 1
    
    return comp

def DFSComp(G, u, c, comp):
    comp[u] = c
    for i in G[u]:
        if comp[i] == -1:
            DFSComp(G, i, c, comp)
            
#%%

def compFort(G):
    n = len(G)
    comp = [-1]*n
    c = 0
    for u in range(n):
        if comp[u] == -1:
            CF(G, u, c, comp)
            c += 1
    
    return comp

def CF(G, u, c, comp):
    n = len(G)
    
    GT = trasponi(G)
    
    A = [0]*n
    B = [0]*n
    
    DFScf(G, u, A)
    DFScf(GT, u, B)
    
    for i in range(n):
        if A[i] == 1 and B[i] == 1:
            comp[i] = c
    
def DFScf(G, u, visitati):
    visitati[u] = 1
    for i in G[u]:
        if visitati[i] == 0:
            DFScf(G, i, visitati)
            
def trasponi(G):
    n = len(G)
    GT = [[] for _ in range(n)]
    for u in range(n):
        for i in G[u]:
            GT[i].append(u)
    
    return GT
    