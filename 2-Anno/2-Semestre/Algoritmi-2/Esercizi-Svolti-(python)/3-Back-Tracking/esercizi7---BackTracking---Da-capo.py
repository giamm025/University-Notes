# -*- coding: utf-8 -*-
"""
Created on Tue May 27 18:47:57 2025

@author: 39324
"""

def es1(n, sol = []):
    
    if len(sol)==n:
        print(''.join(sol))
        return
    
    sol.append('b')
    es1(n, sol)
    sol.pop()
    
    rimasti = n-len(sol)
    if rimasti>=2:
        sol.append('a')
        sol.append('a')
        es1(n, sol)
        sol.pop()
        sol.pop()
    
es1(5)



#%% 
def es2(n, sol =[], numA = 0):
    
    if n%2 == 1:
        return 
    
    if len(sol) == n:
        print(''.join(sol))
        return
    
    #fino all'ultima posizione posso aggiungere qualsiasi cosa
    if len(sol) < n-1:
        sol.append('a')
        es2(n, sol, numA+1)
        sol.pop()
        
        sol.append('b')
        es2(n, sol, numA)
        sol.pop()
    
    #in ultima posizione 
    else:
        
        #se il numero di a è pari => numero di b è dispari
        if numA%2 == 0:
            #devo inserire una 'a'
            sol.append('a')
            es2(n, sol, numA+1)
            sol.pop()
        
        #se il numero di a è dispari => numero di b è pari
        else:
            #devo inserire una 'b'
            sol.append('b')
            es2(n, sol, numA)
            sol.pop()

es2(4)

#%%

def es3(n, sol = []):
    
    if len(sol)==n:
        copia = sol.copy()
        copia.reverse()
        print(''.join(sol) + ''.join(copia))
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
        
        if len(sol)==0 or (i != sol[-1]+1 and i != sol[-1]-1 and i != sol[-1]):
            sol.append(i)
            es4(n, sol)
            sol.pop()

es4(3)


#%%

def es5(n):
    presi = [0]*(n+1)
    es5r(n, presi)

def es5r(n, presi, sol = []):
    
    if len(sol)==n:
        copia = [str(x) for x in sol]
        print(''.join(copia))
        return
    
    for i in range(1, n+1):
        
        if presi[i]==0 and (len(sol)==0 or (sol[-1]%2 != i%2)):
            presi[i] = 1
            sol.append(i)
            es5r(n, presi, sol)
            sol.pop()
            presi[i] = 0

es5(4)


#%%

def es6(n, m, k):
    count = [0]*(m+1)
    es6r(n, m, k, count)

def es6r(n, m, k, count, sol = []):
    
    if len(sol) == n:
        copia = [str(x) for x in sol]
        print(','.join(copia))
        return
    
    for x in range(1, m+1):
        
        if count[x]<k:
            sol.append(x)
            count[x] += 1
            es6r(n, m, k, count, sol)
            sol.pop()
            count[x] -= 1

es6(3, 2, 2)

#%%

def es7(n):
    sol = [[None for _ in range(n)] for _ in range(n)]
    es7r(n, sol)

def es7r(n, sol, i=0, j=0):
    
    if i==n:
        for riga in sol:
            print(riga)
        print()
        return
    
    i1, j1 = i, j+1
    if j1 == n:
        i1, j1, = i+1, 0
    
    for x in ['a', 'b', 'c']:
        
        if sol[i][0] == None or x == sol[i][0]:
            sol[i][j] = x
            es7r(n, sol, i1, j1)
            sol[i][j] = None
            
es7(2)


#%%

def es8(n):
    sol = [[None for _ in range(n)] for _ in range(n)]
    es8r(n, sol)
    
def es8r(n, sol, i=0, j=0):
    
    if i==n:
        for riga in sol:
            print(riga)
        print()
        return
    
    i1, j1 = i, j+1
    if j1 == n:
        i1, j1 = i+1, 0
    
    for x in [1, 2, 3]:
        
        if (i==0 or sol[i-1][j] <= x) and (j==0 or sol[i][j-1] <= x):
            sol[i][j] = x
            es8r(n, sol, i1, j1)

es8(2)



#%%

def es9(n):
    sol = [[None for _ in range(n)] for _ in range(n)]
    es9r(n, sol)

def es9r(n, sol, i=0, j=0, count = [0]):
    
    if i==n:
        count[0] += 1
        for riga in sol:
            print(riga)
        print('count: ' + str(count[0]))
        print()
        return
    
    i1, j1 = i, j+1 
    if j1==n:
        i1, j1 = i+1, 0
    
    #zero lo posso sempre aggiungere
    sol[i][j] = 0
    es9r(n, sol, i1, j1, count)
    
    #per aggiungere 1 devo assicurarmi che non ci siano altri uni a sx, a dx o in diagonale
    #EDIT: Va considerata anche la diagonale secondaria. quella che guarda le celle in alto a destra
    if (i==0 or sol[i-1][j] != 1) and (j==0 or sol[i][j-1] != 1) and\
       (i==0 or j==0 or sol[i-1][j-1] != 1) and (i==0 or j==n-1 or sol[i-1][j+1] != 1):
        sol[i][j] = 1
        es9r(n, sol, i1, j1, count)

es9(3)