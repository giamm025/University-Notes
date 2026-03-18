# -*- coding: utf-8 -*-
"""
Created on Wed May 21 22:48:59 2025

@author: 39324
"""

def es2(n, sol = [], numDispari1 = 0, numDispari2 = 0):
    
    if len(sol)==2*n:
        copia = [str(x) for x in sol]
        print(''.join(copia))
        return
    
    rimasti = (2*n) - len(sol)
    for i in [1, 2, 3]:
        
        #se sono nella prima metà sol[0:n-1] posso mettere qualsiasi numero
        if len(sol) < n:
            sol.append(i)
            if i%2 == 1:
                es2(n, sol, numDispari1+1)
            else:
                es2(n, sol, numDispari1)
            sol.pop()
        
        #sono nella seconda metà
        else:
            #se ho gia raggiunto il numero di dispari => devo inserire solo pari
            if numDispari1 == numDispari2:
                if i%2 == 0:
                    sol.append(i)
                    es2(n, sol, numDispari1, numDispari2)
                    sol.pop()
            
            #se mi sono rimasti tanti slot quanti sono i numeri dispari che devo
            #ancora inserire => inserisco tutti dispari
            elif rimasti == numDispari1 - numDispari2:
                if i%2 == 1:
                    sol.append(i)
                    es2(n, sol, numDispari1, numDispari2+1)
                    sol.pop()
            
            #se c'è abbastanza spazio inserisco un numero qualsiasi (segnando se è pari o dispari)
            else:
                sol.append(i)
                if i%2 == 1:
                    es2(n, sol, numDispari1, numDispari2+1)
                else:
                    es2(n, sol, numDispari1, numDispari2)
                sol.pop()

es2(2)
        


#%% ALTERNATIVA leggermente piu chiara

def es2(n, sol = [], numDispari = 0, count = [0]):
    
    if len(sol) == (2*n):
        count[0]+=1
        copia = [str(x) for x in sol]
        print(''.join(copia))
        return count

    for i in [1, 2, 3]:
        
        #Sono nella prima metà
        if len(sol) < n:
            
            #inserisco tutto a caso e mi segno quanti dispari inserisco
            sol.append(i)
            if i%2 == 1:
                es2(n, sol, numDispari+1, count)
            else:
                es2(n, sol, numDispari, count)
            sol.pop()
        
        #Sono nella seconda metà => devo compensare i dispari
        #Ogni volta ch einserisco un dispari faccio numDispari-1. Quando numDispari == 0 ho finito ed inserisco solo numeri pari
        else:

            rimasti = (2*n)-len(sol)
            if rimasti == numDispari:
                #aggiungo solo numeri dispari
                if i%2 == 1:
                    sol.append(i)
                    es2(n, sol, numDispari-1, count)
                    sol.pop()
            
            elif numDispari == 0:
                #aggiungo solo numeri pari
                if i%2 == 0:
                    sol.append(i)
                    es2(n, sol, numDispari, count)
                    sol.pop()
            
            elif rimasti > numDispari:
                #aggiungo qualsiasi cosa segnando quali sono dispari e quali pari
                sol.append(i)
                if i%2 == 1:
                    es2(n, sol, numDispari-1, count)
                else:
                    es2(n, sol, numDispari, count)
                sol.pop()
        
    return count

print(es2(2))
