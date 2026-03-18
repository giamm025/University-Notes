# -*- coding: utf-8 -*-
"""
Created on Thu May 15 11:53:42 2025

@author: 39324
"""

def es12(S):
    n = len(S)
    T = [S[i] for i in range(n)]
    massimo = T[0]                      #contiene il massimo di T[0:i-2]
    for i in range(2, n):
        T[i] += massimo
        massimo = max(massimo, T[i-1])  #al prossimo passo 
    
    return max(T)

#Analoga alla funzione sopra ma con codice piu chiaro (anche se piu lungo)
def es12B(S):
    n = len(S)
    T = [None]*n
    
    T[0], T[1] = S[0], S[1]
    
    massimo = T[0]                      #contiene il massimo di T[0:i-2]
    for i in range(2, n):
        T[i] = massimo + S[i]           #T[i] = max{T[0], ..., T[i-2]} + S[i]
        massimo = max(massimo, T[i-1])  #al prossimo passo 
    
    return max(T)

def es12Chat(S):
    n = len(S)
    T = [None]*n
    T[0] = S[0]
    T[1] = max(T[0], S[1])
    for i in range(2, n):
        T[i] = max(T[i-1], T[i-2] + S[i])
    
    return T[n-1]


S = [3, 2, 5, 10, 7]
print(es12(S))
print(es12Chat(S))