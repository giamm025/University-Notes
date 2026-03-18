# -*- coding: utf-8 -*-
"""
Created on Tue May 20 12:15:34 2025

@author: 39324
"""

def es1(n, sol = [], aperte = 0):
    if len(sol) == 2*n:
        print(''.join(sol))
        return
    
    #se ho piu di n parentesi aperte le altre n-1 posizioni non basteranno a chiuderle tutte
    #quindi aggiungo ( finche non arrivo ad n. Poi devo mettere solo )
    chiuse = len(sol) - aperte
    if aperte < n:
        sol.append('(')
        es1(n, sol, aperte+1)
        sol.pop()
    
    #se aggiungendo ) chiudo piu parentesi di quante ne ho aperte => stringa non valida
    if chiuse < aperte:
        sol.append(')')
        es1(n, sol, aperte)
        sol.pop()    

es1(3)


#Cosi stampa tutte le sequenze CON ordine. Invece la consegna dice SENZA
#quindi bosgna tagliare in modo tale che se ho gia stampato 1, 1, 2 non stampi 1, 2, 1
def es2(n, sol=[], somma = 0):
    
    if somma == n:
        copia = [str(x) for x in sol]
        print(','.join(copia))
        return
    
    for i in range(1, n+1):
        #se aggiungendo l'elemento supero la somma => NON lo aggiungo
        #per rimuovere le ripetizioni (e quindi stampare le sequenze SENZA ordine)
        #aggiungiamo solo le sequenze "crescenti". Quindi 1,1,2 e non 1,2,1
        if somma + i <= n and (len(sol)==0 or i >= sol[-1]):
            sol.append(i)
            es2(n, sol, somma+i)
            sol.pop()

es2(4)