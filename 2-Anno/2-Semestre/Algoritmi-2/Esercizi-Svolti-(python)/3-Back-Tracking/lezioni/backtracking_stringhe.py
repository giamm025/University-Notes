# -*- coding: utf-8 -*-
"""
Created on Mon May 12 15:27:10 2025

@author: 39324
"""

def es3(n, sol = []):
    if len(sol) == n:
        print(''.join(sol)) #converte la lista in stringa
        return 
    
    sol.append(0)
    es3(n, sol)
    sol.pop()
    
    if len(sol)<2 or sol[-1]==0 or sol[-2]==0:
        sol.append(1)
        es3(n, sol)
        sol.pop()
        
        
        
        