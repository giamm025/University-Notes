# -*- coding: utf-8 -*-
"""
Created on Thu May 22 10:52:06 2025

@author: 39324
"""

def es3(n, sol = []):
    
    if len(sol) == n:
        copia = [str(x) for x in sol]
        print(''.join(copia))
        return
    
    for i in [0, 1, 2]:
        
        #posso sempre aggiungere un numero dispari
        if i%2 == 1:
            sol.append(i)
            es3(n, sol)
            sol.pop()
            
        #per inserire un numero dispari devo prima contrllare che il suo adiacente sia dispari
        elif len(sol)==0 or sol[-1]%2 != 0:
            sol.append(i)
            es3(n, sol)
            sol.pop()

es3(1)
es3(2)