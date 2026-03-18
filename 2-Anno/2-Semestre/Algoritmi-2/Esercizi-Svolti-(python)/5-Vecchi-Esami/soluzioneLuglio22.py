# -*- coding: utf-8 -*-
"""
Created on Thu May 22 11:48:33 2025

@author: 39324
"""

def es2(n, k, sol = [], numZeri = 0):
    
    if len(sol) == n:
        copia = [str(x) for x in sol]
        print(''.join(copia))
        return
    
    rimasti = n-len(sol)
    for i in [0, 1]:
        
        #se il numero di posti rimasti è uguale al numero di zeri che devo ancora mettere
        if rimasti == k-numZeri:
            #posso mettere solo 0
            if i == 0:    
                sol.append(i)
                es2(n, k, sol, numZeri+1)
                sol.pop()
        
        #se non ho gia raggiunto il numero minimo di zeri AND
        #l'aggiunta  di un 1 mi fa rimanere un numero di posizioni < del numero di zeri che mi servono => devo mettere 0
        elif numZeri<k and rimasti-1 < k:
            #posso mettere solo 0
            if i == 0:    
                sol.append(i)
                es2(n, k, sol, numZeri+1)
                sol.pop()    
        
        else:
            if i == 0:    
                sol.append(i)
                es2(n, k, sol, numZeri+1)   #incremento il numero di zero consecutivi (se il numero prima era un 1 numZeri è gia stato resettato a 0)
                sol.pop()
            else:   
                sol.append(i)
                es2(n, k, sol, numZeri=0)   #ogni volta che metto un 1 il numero di 0 consecutivi va resettato
                sol.pop()
    
es2(4, 2) 
    