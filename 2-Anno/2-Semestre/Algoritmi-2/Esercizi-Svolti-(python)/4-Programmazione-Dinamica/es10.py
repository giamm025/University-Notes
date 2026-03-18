# -*- coding: utf-8 -*-
"""
Created on Wed May 14 09:47:54 2025

@author: 39324
"""
    
def es10(X, s):
    n = len(X)
    T = [[0 for _ in range(s+1)] for _ in range(n)]
    massimo = [0]*(s+1)
    for i in range(n):
        riga = []
        for j in range(s+1):
            
            if X[i] == j:
                T[i][j] = 1 
            
            elif j-X[i] >= 0:
                T[i][j] = massimo[j-X[i]] + 1
                
            riga.append(T[i][j])
        
        for j in range(s+1):
            massimo[j] = max(massimo[j], riga[j])
        
    return max([T[i][s] for i in range(n)])

def es10b(X, s):
    n = len(X)
    T = [[0 for _ in range(s+1)] for _ in range(n)]
    for i in range(n):
        for j in range(s+1):
            
            if X[i] == j:
                T[i][j] = 1 
            
            elif j-X[i] >= 0 and i>0:
                T[i][j] = 1 + max(T[k][j-X[i]] for k in range(i))
                
    return max([T[i][s] for i in range(n)])


X = [5, 2, 2, 6, 1, 7, 3, 5, 11, 3, 6]
print(es10b(X, 25))

X1 = [3, 3, 5, 13, 3, 5]
print(es10b(X1, 28))
