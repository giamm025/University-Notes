# -*- coding: utf-8 -*-
"""
Created on Thu May 15 17:00:07 2025

@author: 39324
"""

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
    
    if (i==0 and j==0) or \
       (i==0 and j>0 and sol[j-1] == 0) or \
       (i>0 and j==0 and sol[i-1] == 0) or \
       (i>0 and j>0 and sol[i-1] == sol[j-1] == 0):
            sol[i][j] = 0
            es1(n, sol, i1, j1)
    
    sol[i][j] = 1
    es1(n, sol, i1, j1)