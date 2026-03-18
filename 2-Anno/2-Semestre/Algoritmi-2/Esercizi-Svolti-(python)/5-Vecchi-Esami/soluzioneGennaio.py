# -*- coding: utf-8 -*-
"""
Created on Fri May 23 21:49:48 2025

@author: 39324
"""

def es2(X, sol = []):
    
    n = len(X)
    if len(sol)==n:
        print(''.join(sol))
        return
    
    for i in ['0', '1', '2']:
        if i != X[len(sol)] and (len(sol)==0 or sol[-1]!=i):
            sol.append(i)
            es2(X, sol)
            sol.pop()
            
es2('2001')