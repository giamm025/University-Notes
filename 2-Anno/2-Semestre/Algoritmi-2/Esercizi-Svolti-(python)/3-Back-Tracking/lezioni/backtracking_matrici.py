# -*- coding: utf-8 -*-
"""
Created on Thu May 15 16:35:14 2025

@author: 39324
"""

#Backtracking sulle Matrici
def es1(n, sol, i = 0, j = 0):
    if i==n:
        for k in range(n):
            print(sol[k])
        print()             #stampa \n
        return
    
    #i1, j1 indicano la prossima cella in cui andare. Mentre i, j la cella attuale
    i1, j1 = i, j+1     
    if j1 == n:
        i1 = i + 1
        j1 = 0
    
    sol[i][j] = 0
    es1(n, sol, i1, j1)
    
    sol[i][j] = 1
    es1(n, sol, i1, j1)
    