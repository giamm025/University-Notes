# -*- coding: utf-8 -*-
"""
Created on Sun May 11 19:04:48 2025

@author: 39324
"""

def es3a(X):
    n = len(X)
    T = [1 for _ in range(n)]
    for i in range(n):
        massimo = 0
        for j in range(i):
            if X[j]<X[i] and T[j]>massimo:
                massimo = T[j]
        T[i] = massimo + 1
        
    return max(T)


def es3b(X):
    n = len(X)
    T = [X[i] for i in range(n)]
    for i in range(n):
        massimo = 0
        for j in range(i):
            if X[j]<X[i] and T[j]>massimo:
                massimo = T[j]
        T[i] = X[i] + massimo
        
    return max(T)


def es3c(X):
    n = len(X)
    T = [1 for _ in range(n)]
    for i in range(n):
        for j in range(i):
            if X[j]<X[i]:
                T[i] += T[j]     
        
    return sum(T)


def es3d(X, k):
    n = len(X)
    T = [[0 for _ in range(k+1)] for _ in range(n)]

    for i in range(n):
        T[i][1] = 1
        
    for i in range(n):  
        for j in range(1, k+1):
            for y in range(i):
                if X[y]<X[i]:
                    T[i][j] += T[y][j-1]
    
    return sum(T[i][k] for i in range(n))
        
