# -*- coding: utf-8 -*-
"""
Created on Sat May 24 16:13:26 2025

@author: 39324
"""

def es2r(n):
    usati = [0]*(n+2)
    es2(n, usati)

def es2(n, usati, sol = []):
    
    if len(sol)==n:
        copia = [str(x) for x in sol]
        print(''.join(copia))
        return
    
    for i in range(1, n+1):
        if usati[i]==0 and (len(sol)==0 or sol[-1]%2 != i%2):
            usati[i] = 1
            sol.append(i)
            es2(n, usati, sol)
            sol.pop()
            usati[i] = 0


es2r(4)



#%%
def es3r(n, k):
    usati = [0]*n
    es3(n, k, usati)
    
def es3(n, k, usati, sol = []):
    
    if len(sol)==n:
        copia = [str(x) for x in sol]
        print(''.join(copia))
        return
    
    #i possibili punti fissi sono tutti i numeri >= len(sol) che non sono ancora stati utilizzati
    possibiliPuntiFissi = usati[len(sol):].count(0)
    for i in range(n):
        
        #posso sempre aggiungere un punto fisso
        if usati[i]==0 and i == len(sol):
            usati[i] = 1
            sol.append(i)
            es3(n, k-1, usati, sol)
            sol.pop()
            usati[i] = 0
        
        #se NON sto aggiungendo un punto fisso devo verificare che dopo ci siano abbastanza numeri
        #per arrivare ad avere almeno k punti fissi
        elif usati[i]==0 and possibiliPuntiFissi >= k:
            usati[i] = 1
            sol.append(i)
            es3(n, k, usati, sol)
            sol.pop()
            usati[i] = 0
            
        #se fossero richiesti ESATTAMENTE k punti fissi avrei dovuto aggiungere un controllo:
        #se ho gia raggiunto k punti fissi => inserisci solo i tc i != len(sol)

es3r(4, 2)