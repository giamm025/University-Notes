# -*- coding: utf-8 -*-
"""
Created on Fri May 23 19:26:31 2025

@author: 39324
"""

def es3r(n):
    sol = [[None for _ in range(n)] for _ in range(n)]
    es3(n, sol)

def es3(n, sol, i=0, j=0, numUni = 0):
    
    if i==n:
        for riga in sol:
            print(riga)
        print()
        return
    
    #ogni volta che cambio riga devo resettare il numero di uni
    if j==0:
        numUni = 0
    
    #calcolo i prossimi indici
    i1, j1 = i, j+1
    if j1==n:
        i1, j1, = i+1, 0
    
    #posso mettere lo 0 solo se poi mi rimangono abbastanza spazi per inserire gli 1 giusti
    rimasti = n-j
    if rimasti-1 >= i-numUni:
        sol[i][j] = 0
        es3(n, sol, i1, j1, numUni)
    
    #aggiungo 1 solo se non sono ancora arrivato ad averne esattamente i
    if numUni < i:
        sol[i][j] = 1
        es3(n, sol, i1, j1, numUni+1)

es3r(3)