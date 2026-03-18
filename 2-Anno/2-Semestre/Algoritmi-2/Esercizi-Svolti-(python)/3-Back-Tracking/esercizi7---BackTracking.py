# -*- coding: utf-8 -*-
"""
Created on Tue May 20 21:24:41 2025

@author: 39324
"""
#%%
def es1(n, sol = []):
    
    if len(sol) == n:
        print(''.join(sol))
        return
    
    sol.append('b')
    es1(n, sol)
    sol.pop()

    if n-len(sol) >= 2:
        sol.append('a')
        sol.append('a')
        es1(n, sol)
        sol.pop()
        sol.pop()

#es1(5)

#%%
def es2(n, sol = [], numA = 0):
    if n%2 == 1:
        return
    
    if len(sol) == n:
        print(''.join(sol))
        return
    
    numB = len(sol)-numA
    if n-len(sol) == 1 and numB%2 == 1:
        sol.append('a')
        es2(n, sol, numA+1)
        sol.pop()
        
    elif n-len(sol) == 1 and numA%2 == 1:
        sol.append('b')
        es2(n, sol, numA)
        sol.pop()
            
    else:
        sol.append('a')
        es2(n, sol, numA+1)
        sol.pop()
    
        sol.append('b')
        es2(n, sol, numA)
        sol.pop()

es2(4)


#%%
def es3(n, sol = []):
    if len(sol) == n:
        sol2 = [x for x in reversed(sol)]
        print(''.join(sol) + ''.join(sol2))
        return
    
    sol.append('a')
    es3(n, sol)
    sol.pop()
    
    sol.append('b')
    es3(n, sol)
    sol.pop()
    
es3(2)

#%%
def es4(n, sol = []):
    if len(sol) == n:
        copia = [str(x) for x in sol]
        print(''.join(copia))
        return
    
    for i in [1, 2, 3, 4]:
        if len(sol)==0 or (sol[-1] != i-1 and sol[-1] != i and sol[-1] != i+1):
            sol.append(i)
            es4(n, sol)
            sol.pop()
            
es4(3)


#%%
def es5(n):
    preso = [0]*(n+1)
    es5r(n, preso)
    
def es5r(n, preso, sol = []):
    if len(sol) == n:
        copia = [str(x) for x in sol]
        print(''.join(copia))
        return
    
    for i in range(1, n+1):
        if preso[i] == 0:
            if len(sol) == 0 or (i%2 != sol[-1]%2):
                sol.append(i)
                preso[i] = 1
                es5r(n, preso, sol)
                sol.pop()
                preso[i] = 0

es5(4)


#%%
def es6(n, m, k):
    count = [0]*(m+1)
    es6r(n, m, k, count)

def es6r(n, m, k, count, sol = []):
    
    if len(sol) == n:
        copia = [str(x) for x in sol]
        print(','.join(copia))
    
    for i in range(1, m+1):
        if count[i] < k:
            sol.append(i)
            count[i] += 1
            es6r(n, m, k, count, sol)
            sol.pop()
            count[i] -= 1

es6(3, 2, 2)

#%%
def es7(n):
    sol = [[0 for _ in range(n)] for _ in range(n)]
    es7r(n, sol)

def es7r(n, sol, i=0, j=0):
    #quando ho superato l'ultima riga stampo
    if i == n:
        for riga in sol:
            print(riga)
        print()
        return
    
    i1, j1 = i, j+1 
    #quando ho superato l'ultima colonna devo tornare a vedere la prima della riga successiva
    if j1 == n:
        i1, j1 = i+1, 0
    
    if j==0:
        for char in ['a', 'b', 'c']:
            sol[i][j] = char
            es7r(n, sol, i1, j1)
    else:
        sol[i][j] = sol[i][j-1]
        es7r(n, sol, i1, j1)

es7(2)

#%%

def es7short(n, sol = []):
    
    if len(sol) == n:
        M = [[x]*n for x in sol]
        for riga in M:
            print(riga)
        print()
        return
    
    for char in ['a', 'b', 'c']:
        sol.append(char)
        es7short(n, sol)
        sol.pop()
    
es7short(2)


#%%
def es8(n):
    sol = [[0]*n for _ in range(n)]
    es8r(n, sol)

def es8r(n, sol, i=0, j=0):
    #CASO BASE
    if i == n:
        for riga in sol:
            print(riga)
        print()
        return

    # Calcola la prossima cella
    i1, j1 = i, j+1
    if j1 == n:
        i1, j1, = i+1, 0

    for x in [1, 2, 3]:

        if (j == 0 or sol[i][j-1] <= x) and (i == 0 or sol[i-1][j] <= x):
            sol[i][j] = x
            es8r(n, sol, i1, j1)


es8(2)


#%%
def es9(n):
    sol = [[0]*n for _ in range(n)]
    es9r(n, sol)

def es9r(n, sol, i=0, j=0, count = [0]):
    #CASO BASE
    if i == n:
        count[0] += 1
        for riga in sol:
            print(riga)
        print(count)
        print()
        return

    # Calcola la prossima cella
    i1, j1 = i, j+1
    if j1 == n:
        i1, j1, = i+1, 0

    #Posso sempre aggiungere zero
    sol[i][j] = 0
    es9r(n, sol, i1, j1, count)
    
    #per aggiungere uno devo controllare
    if (i==0 or sol[i-1][j] != 1) and (j==0 or sol[i][j-1] != 1) \
       and (i==0 or j==0 or sol[i-1][j-1] != 1):
           sol[i][j] = 1 
           es9r(n, sol, i1, j1, count)
           
es9(2)
