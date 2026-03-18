# -*- coding: utf-8 -*-
"""
Created on Fri May 23 17:21:35 2025

@author: 39324
"""

def es2r(n):
                  #0      1        2         3        4            5           6         7          8         9
    tastierino = [[8], [2, 4], [1, 3, 5], [2, 6], [1, 5, 7], [2, 4, 6, 8], [3, 5, 9], [4, 8], [0, 5, 7, 9], [6, 8]] 
    es2(n, tastierino)

def es2(n, tastierino, sol = []):
    
    if len(sol)==n:
        copia = [str(x) for x in sol]
        print(''.join(copia))
        return
    
    for i in range(10):
        
        #se sol è vuota posso aggiungere un numero qualsiasi
        if len(sol)==0:
            sol.append(i)
            es2(n, tastierino, sol)
            sol.pop()
        
        elif sol[-1]==i:
            for vicino in tastierino[i]:
                sol.append(vicino)
                es2(n, tastierino, sol)
                sol.pop()

es2r(2)