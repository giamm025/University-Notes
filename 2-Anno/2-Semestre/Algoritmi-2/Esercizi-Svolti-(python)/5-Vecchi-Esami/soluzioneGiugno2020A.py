# -*- coding: utf-8 -*-
"""
Created on Fri May 23 19:38:40 2025

@author: 39324
"""

def es2(M, sol = [], i=0, j=0):
    
    n = len(M)
    if i==n:
        print(sol)
        return
    
    sol.append(M[i][j])
    es2(M, sol, i+1, j)
    sol.pop()
    
    if j-1 >= 0:
        sol.append(M[i][j-1])
        es2(M, sol, i+1, j-1)
        sol.pop()
    
    if j+1 < n:
        sol.append(M[i][j-1])
        es2(M, sol, i+1, j+1)
        sol.pop()
    

M = [[1, 2],
     [3, 4]]
es2(M)