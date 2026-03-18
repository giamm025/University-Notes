# -*- coding: utf-8 -*-
"""
Created on Sat May 24 14:58:48 2025

@author: 39324
"""

def es1(X, sol = []):
    
    n = len(X)
    if len(sol)==n:
        print(''.join(sol))
        return
    
    for i in ['0', '1', '2']:
        
        if i != X[len(sol)]:
            sol.append(i)
            es1(X, sol)
            sol.pop()

es1('020')

#%%
def es2(n, sol = []):
    
    if len(sol)==n:
        print(''.join(sol))
        return
    
    for i in ['0', '1']:
        
        if len(sol)<2 or i!=sol[-2] or i!=sol[-1]:
            sol.append(i)
            es2(n, sol)
            sol.pop()
            
es2(3)

#%%
def es3(n, a, sol = [], numUni = 0):
    
    if len(sol)==n:
        print(''.join(sol))
        return
    
    numZeri = len(sol) - numUni
    vantaggio = numUni - numZeri
    
    #se aggiugendo questo 0 il vantaggio va ancora bene => aggiungo 
    if -a <= vantaggio-1 <= a:
        sol.append('0')
        es3(n, a, sol, numUni)
        sol.pop()
    
    #se aggiugendo questo 1 il vantaggio va ancora bene => aggiungo 
    if -a <= vantaggio+1 <= a:
        sol.append('1')
        es3(n, a, sol, numUni+1)
        sol.pop()
        
es3(5, 2)