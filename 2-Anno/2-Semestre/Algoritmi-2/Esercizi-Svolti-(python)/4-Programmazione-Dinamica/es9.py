# -*- coding: utf-8 -*-
"""
Created on Mon May 12 22:23:22 2025

@author: 39324
"""

def es9(A):
    n = len(A)
    
    indici = [None] * (n*n+1)   #+1 perche i valori dentro A vanno da 1 a n^2. Non da 0 ad n^2-1
    for i in range(n):
        for j in range(n):
            indici[A[i][j]] = (i, j)
    
    T = [[1 for _ in range(n)] for _ in range(n)]
    #inizio a riempire la tabella in ordine crescente! dal piu piccolo al piu grande. altrimenti non funziona nulla
    for v in range(1, n*n+1):
        i, j = indici[v]
        if i>0 and A[i-1][j] == A[i][j]-1:
            T[i][j] += T[i-1][j]
            
        if i<n-1 and A[i+1][j] == A[i][j]-1:
            T[i][j] += T[i+1][j]
            
        if j>0 and A[i][j-1] == A[i][j]-1:
            T[i][j] += T[i][j-1]
            
        if j<n-1 and A[i][j+1] == A[i][j]-1:
            T[i][j] += T[i][j+1]
        
        #se non entro in nessuno degli altri casi T[i][j] rimane inizializzato ad 1
        #poiche l'unico percorso che mi porta a quella cella è quello che comprende il valore stesso
    
    return max(max(riga) for riga in T)


B = [[9, 7, 6], [8, 2, 5], [1, 3, 4]]
print(es9(B))
        