# -*- coding: utf-8 -*-
"""
Created on Sun May 11 21:52:08 2025

@author: 39324
"""

def es4(M):
    n = len(M)
    m = len(M[0])
    
    T = [[M[i][j] for j in range(m)] for i in range(n)]
    
    for i in range(1, n):                   #O(n)
        for j in range(m):                  #O(m)
            T[i][j] += max(T[i-1][:j+1])    #Questo mi fa salire la complessità ad O(n*m^2)
    
    
    return max(max(riga) for riga in T)


#SOLUZIONE: per ridurre la complessità ci precalcoliamo il massimo di ogni riga fino alla colonna j.
def es4Corretto(M):
    n = len(M)
    m = len(M[0])
    
    T = [[M[i][j] for j in range(m)] for i in range(n)]
    
    
    max_left = [0] * m
    for i in range(1, n):           #O(n)
        
        #riempiamo max left
        max_left[0] = T[i-1][0]
        for j in range(1, m):       #O(m)
            #il massimo fino alla colonna j-esima è il maggiore fra il massimo accumulato fino ad ora ed il valore corrente
            max_left[j] = max(max_left[j-1], T[i-1][j])
            
        for j in range(m):          #O(m) ma è staccato dall'altro!
            T[i][j] += max_left[j]
    
    
    return max(max(riga) for riga in T)

#Abbiamo quindi costo = O(n)*(O(m) + O(m)) = O(n) * O(m) = O(n*m)