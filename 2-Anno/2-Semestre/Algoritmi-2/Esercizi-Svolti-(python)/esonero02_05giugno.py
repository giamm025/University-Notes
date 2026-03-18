# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 15:20:23 2025

@author: 39324
"""

def es1(n):
    
    T = [[None]*3 for _ in range(n+1)]
    
    for i in range(1, n+1):
        for j in range(3):
            
            if i==1:
                T[i][j] = 1
            
            elif j==0 or j==1:
                T[i][j] = T[i-1][0] + T[i-1][1] + T[i-1][2]
            
            else: #se j==2
                T[i][j] = T[i-1][0]
    
    return sum(T[n])
    

print(es1(3))

def es2(n):
    sol = [[None for _ in range(n)] for _ in range(n)]
    es2r(n, sol)
    
def es2r(n, sol, i=0, j=0, numUni=0, count = [0]):
    
    if i==n:
        count[0] += 1
        for riga in sol:
            print(riga)
        print(count)
        print()
        return
    
    i1, j1 = i, j+1
    if j1==n:
        i1, j1 = i+1, 0
    
    if j==0:
        numUni = 0
    
    rimasti = n-j
    if numUni%2 == 0 or rimasti-1 > 0:
        sol[i][j] = 0
        es2r(n, sol, i1, j1, numUni, count)
    
    if numUni%2 == 1 or rimasti >= 2:
        sol[i][j] = 1
        es2r(n, sol, i1, j1, numUni+1, count)
        
# es2(3)
    