# -*- coding: utf-8 -*-
"""
Created on Sat May 24 10:07:54 2025

@author: 39324
"""

def domanda3r(X):
    sol = [None]*len(X)
    domanda3(X, sol)
    

def domanda3(X, sol = [], i = 0, numZeri = 0):
    
    return



#%%
def es3(X, k, sol = []):
    
    n = len(X)
    if len(sol)==n:
        print(''.join(sol))
        return
    
    rimasti = n-len(sol)
    for i in ['0', '1']:
        
        #aggiungo elementi diversi solo finche posso. quando k==0 devo aggiungere solo elementi uguali
        if i!=X[len(sol)] and k>0:
            sol.append(i)
            es3(X, k-1, sol)
            sol.pop()
        
        #se k==0 ho gia raggiunto l'obiettivo e devo aggiungere solo elementi uguali
        elif k==0 and i==X[len(sol)]:
            sol.append(i)
            es3(X, k, sol)
            sol.pop()
            
        #aggiungo un elemento uguali solo se la sua aggiunta mi lascia comunqeu abbastanza spazio per compensare i k elementi diversi
        elif i==X[len(sol)] and rimasti-1 >= k:
            sol.append(i)
            es3(X, k, sol)
            sol.pop()
            

es3('1101', 2)