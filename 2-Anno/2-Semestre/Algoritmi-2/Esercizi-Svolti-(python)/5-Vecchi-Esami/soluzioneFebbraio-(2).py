# -*- coding: utf-8 -*-
"""
Created on Wed May 21 20:20:10 2025

@author: 39324
"""

def es2(n):
    sol = [[None for _ in range(n)] for _ in range(n)]
    es2r(n, sol)

#conviene scorrere per colonne invece che per righe. quindi scambio tutte le i e le j
def es2r(n, sol, i = 0, j = 0, numZeri = 0):
    
    if j == n:
        for riga in sol:
            print(riga)
        print()
        return
    
    #resetto il numero di zero ogni volta che cambio colonna (cioè ogni volta che riparto dalla prima riga)
    if i == 0:
        numZeri = 0
    
    i1, j1 = i+1, j
    if i1 == n:
        i1, j1 = 0, j+1
    
    restanti = n-i              #numero di riga rimaste da riempire
    #se metto lo zero devo assicurare che ci siano abbastanza 'restanti' per compensare con gli uno
    if numZeri < restanti:
        sol[i][j] = 0
        es2r(n, sol, i1, j1, numZeri+1)
    
    sol[i][j] = 1
    es2r(n, sol, i1, j1)

es2(2)