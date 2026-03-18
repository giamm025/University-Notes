# -*- coding: utf-8 -*-
"""
Created on Fri May 16 14:36:15 2025

@author: 39324
"""

''' Stampare tutte le stringhe ternarie (cioe con simboli da 0 a 2)
    che NON hanno mai 3 numeri consecutivi la cui somma è pari
'''
def es2(n, sol = []):
    if len(sol) == n:
        copy = [str(x) for x in sol]
        print(''.join(copy))
        return
    
    for i in range(3):
        #se la somma degli ultimi 3 elementi sarebbe dispari va bene
        if len(sol) < 2 or (sol[-2] + sol[-1] + i)%2 == 1:
            sol.append(i)
            es2(n, sol)
            sol.pop()
        #se invece non va bene passo direttamente al prossimo simbolo
        #(che sicuramente andra bene, perche se prima la somma era pari ora diventra dispari)
es2(4)
    