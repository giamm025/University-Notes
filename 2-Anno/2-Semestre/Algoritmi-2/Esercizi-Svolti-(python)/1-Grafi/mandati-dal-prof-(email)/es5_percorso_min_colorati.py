# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 10:40:53 2025

@author: 39324
"""

def es5(G, C, a, b):
    n = len(G)
    distanza = [None]*n
    distanza[a] = 0
    coda = [a]
    i = 0
    while i < len(coda):
        u = coda[i]
        i += 1
        for v in G[u]:
            if distanza[v] == None and C[v] != C[u]:
                coda.append(v)
                distanza[v] = distanza[u] +1
    
    return distanza[b]

G = [[1, 2, 3], [0, 4, 5, 6], [0, 6], [0, 4], [1, 3, 5], [1, 4, 6], [1, 2, 5]]
C = [0, 0, 1, 1, 1, 3, 0]
print(es5(G, C, 0, 1))