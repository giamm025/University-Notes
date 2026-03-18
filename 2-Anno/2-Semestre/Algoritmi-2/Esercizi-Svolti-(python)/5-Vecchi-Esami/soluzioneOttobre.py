# -*- coding: utf-8 -*-
"""
Created on Thu May 22 10:13:37 2025

@author: 39324
"""


def es2(n, sol = [], numZeri1 = 0, numUni2 = 0):
    
    if len(sol) == (2*n):
        copia = [str(x) for x in sol]
        print(''.join(copia))
        return
    
    rimasti = (2*n) - len(sol)
    for i in [0, 1]:
        #nella prima metà posso aggiungere quello che voglio
        if len(sol) < n:
            sol.append(i)
            if i==0:
                es2(n, sol, numZeri1+1)
            else:
                es2(n, sol, numZeri1)
            sol.pop()
        
        #nella seconda metà:
        else:
            #posso sempre aggiungere gli uno
            if i==1:
                sol.append(i)
                es2(n, sol, numZeri1, numUni2+1)
                sol.pop()
            
            #zero lo posso aggiungere solo se il numero di posizioni rimaste mi consentirà
            #comunque di inserire abbastanza 1 da compensare gli 0 della prima metà di stringa
            elif rimasti > numZeri1 - numUni2:
                sol.append(i)
                es2(n, sol, numZeri1, numUni2)
                sol.pop()
  
es2(2)   
        