# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 15:19:47 2025

@author: 39324
"""

def es3(n, sol=[], numA=0, numB=0):
    
    if len(sol) == n:
        print(''.join(sol) + ": " + str(numA) + ", " +  str(numB))
        return
    
    rimasti = n-len(sol)
    
    aNecessarie = numB-numA
    bNecessarie = numA-numB
    
    #se mi è rimasto un numero di posizioni esattamente uguale alle aNecessarie
    if rimasti == aNecessarie:
        #inserisco solo a fino a compensare le b
        sol.append('a')
        es3(n, sol, numA+1, numB)
        sol.pop()
        
    #se mi è rimasto un numero di posizioni esattamente uguale alle bNecessarie
    elif rimasti == bNecessarie:
        #inserisco solo a fino b compensare le a
        sol.append('b')
        es3(n, sol, numA, numB+1)
        sol.pop()
    
    else:
        
        #dobbiamo controllare che aggiungendo un 'a' rimanga abbastanza spazio per compensare con le 'b'
        if rimasti-1 >= bNecessarie+1:
            sol.append('a')
            es3(n, sol, numA+1, numB)
            sol.pop()
        
        #dobbiamo controllare che aggiungendo un 'b' rimanga abbastanza spazio per compensare con le 'a'
        if rimasti-1 >= aNecessarie+1:
            sol.append('b')
            es3(n, sol, numA, numB+1)
            sol.pop()
        
        #qui siamo gia sicuri di poter aggiuncere le 'c' perche senno saremmo caduti in uno dei due if iniziali
        sol.append('c')
        es3(n, sol, numA, numB)
        sol.pop()

es3(3)