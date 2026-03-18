# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 14:17:51 2025

@author: 39324
"""

def es1(A, s, t):
    n = len(A)
    G = trasforma(A)
    
    u = A.index(s)
    padre = [-1]*n
    padre[u] = u
    coda = [u]
    i = 0
    while i < len(coda):
        u = coda[i]
        i += 1
        for v in G[u]:
            if padre[v] == -1:
                padre[v] = u
                coda.append(v)
    
    y = A.index(t)
    cammino = []
    while y != padre[y]:
        cammino.append(A[y])
        y = padre[y]
    
    cammino.append(s)
    cammino.reverse()
    return cammino
        
        
        

def trasforma(A):
    n = len(A)
    l = len(A[0])
    G = [[] for _ in range(n)]
    for i in range(n):
        u = A[i]
        for j in range(n):
            v = A[j]
            diverse = 0
            for k in range(l):
                if u[k] != v[k]:
                    diverse += 1        #conto le lettere diverse
            
            if diverse == 1:            #se hanno una sola lettera diversa posso passare da una all'altra
                G[i].append(j)
    
    print(G)
    return G
            
A = ["dote", "rata", "cave", "data", "cate", "rapa", "cane", "core", "rate", "cose"]
print(es1(A, "cane", "data"))