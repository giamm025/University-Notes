# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 19:00:03 2025

@author: 39324
"""

def es3(M):
    n = len(M)
    porte = []
    
    #trovo le porte su prima e utila riga (facendo scorrere le colonne)
    for i in [0, n-1]:
        for j in range(n):
            if M[i][j] == 0:
                porte.append((i, j))
    
    for j in [0, n-1]:
        for i in range(n):
            if M[i][j] == 0:
                porte.append((i, j))
    
    #trovo le porte su prima e utila colonna (facendo scorrere le righe)
    count = 0
    for (i, j) in porte: 
        count += DFS(M, i, j)
        
    return count


def DFS(M, i, j):
    
    if M[i][j] == 1:
        return 0

    M[i][j] = 1
    count = 1
    
    #conto gli zero sopra di me
    if i-1>=0:
        count += DFS(M, i-1, j)
    
    #conto gli zero a sinistra
    if j-1>=0:
        count += DFS(M, i, j-1)
    
    #conto gli zero a destra
    if j+1<len(M):
        count += DFS(M, i, j+1)
    
    #conto gli zero sotto di me
    if i+1<len(M):
        count += DFS(M, i+1, j)
    
    return count


M = [[1, 1, 0, 1, 1, 0, 1],
     [1, 0, 0, 0, 0, 0, 1],
     [1, 1, 0, 1, 1, 1, 1],
     [1, 1, 1, 0, 1, 0, 1],
     [0, 0, 1, 0, 1, 0, 1],
     [1, 0, 1, 1, 1, 0, 1],
     [1, 0, 1, 0, 1, 1, 1]]

print(es3(M))