# -*- coding: utf-8 -*-
"""
Created on Wed May 21 21:17:50 2025

@author: 39324
"""

def es1(M):
    n = len(M)
    T = [[0 for _ in range(n)] for _ in range(n)]
    T[0][0] = 1
    for i in range(n):
        for j in range(n):
               
            if i!= 0 and M[i-1][j] != M[i][j]:
               T[i][j] += T[i-1][j]
               
            if j!=0 and M[i][j-1] != M[i][j]:
               T[i][j] += T[i][j-1]

    return T[n-1][n-1]

M = [[1, 0, 1], 
     [0, 1, 0], 
     [0, 1, 1]]
print(es1(M))

M = [[1, 1, 0], 
     [0, 0, 0], 
     [1, 0, 1]]
print(es1(M))


def es2(X, sol = [], numUguali = 0):
    n = len(X)
    if len(sol) == n:
        print(''.join(sol))
        return
    
    for i in ['0', '1', '2']:
        #se sono arrivato all'ultimo elemento ed ho ancora 0 elementi uguali => devo per forza metterne uno uguale
        #(senza questa parte stampavo tutte le stringhe con al piu 1 elemento uguale... invece serve esattamete uno)
        if len(sol) == n-1 and numUguali == 0:
            if i==X[len(sol)]:
                sol.append(i)
                es2(X, sol, numUguali+1)
                sol.pop()
            else:
                continue
        
        #posso sempre mettere un elemento diverso (tranne se sono in ultima posizione, ma lo gestisco con l'if prima)
        elif i!=X[len(sol)]:
            sol.append(i)
            es2(X, sol, numUguali)
            sol.pop()
        
        #se l'elemento che voglio aggiungere è uguale a quello in X devo controllare che non ci sia gia un altro numero uguale
        elif numUguali==0:
            sol.append(i)
            es2(X, sol, numUguali = 1)
            sol.pop()

es2('200')