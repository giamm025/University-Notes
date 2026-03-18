# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 15:37:56 2025

@author: 39324
"""

def es2(G, s):
    n = len(G)
    distanza = [float('inf')]*n
    distanza[s] = 0
    
    coda = [s]
    i = 0
    while i<len(coda):
        u = coda[i]
        i += 1
        for v, c in G[u]:
            if distanza[v]==float('inf'):
                coda.append(v)
                
            nuova = distanza[u]+c
            distanza[v] = min(nuova, distanza[v])            
            
    return distanza


G = [[(2, 1), (3, 2), (5, 4)],  #0
     [(0, 5), (3, 1)],          #1
     [],                        #2
     [(2, -3), (5, 6)],         #3
     [(1, 6),(2,-2)],           #4
     [],                        #5
     []                         #6
     ]    
       
print(es2(G, 0))
print(es2(G, 4))
print(es2(G, 2))