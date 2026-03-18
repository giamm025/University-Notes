# -*- coding: utf-8 -*-
"""
Created on Thu May 22 11:38:14 2025

@author: 39324
"""

# def es2(n, m, k, sol = [], num1 = 0, num2 = 0):
    
#     if len(sol) == n:
#         copia = [str(x) for x in sol]
#         print(''.join(copia))
#         return
    
#     for i in [0, 1, 2]:
        
#         #posso sempre aggiungere zero
#         if i==0:
#             sol.append(i)
#             es2(n, m, k, sol, num1, num2)
#             sol.pop()
        
#         #posso aggiungere 1 solo se la sua aggiunta non supera m
#         if i==1 and num1+1 <= m:
#             sol.append(i)
#             es2(n, m, k, sol, num1+1, num2)
#             sol.pop()
            
#         #posso aggiungere 2 solo se la sua aggiunta non supera k
#         if i==2 and num2+1 <= k:
#             sol.append(i)
#             es2(n, m, k, sol, num1, num2+1)
#             sol.pop()

# es2(3, 1, 2)




'''
                                    Migliore Leggibilità
ogni volta che inseriamo un 1 decrementiamo m ed ogni volta che inseriamo un 2 decrementiamo k
quando m==0 abbiamo inserito tutti gli 1 possibili, quando k=== abbiamo inserito tutti i 2 possibili
'''
def es2r(n, m, k, sol = []):
    
    if len(sol) == n:
        copia = [str(x) for x in sol]
        print(''.join(copia))
        return
    
    for i in [0, 1, 2]:
        
        #posso sempre aggiungere zero
        if i==0:
            sol.append(i)
            es2r(n, m, k, sol)
            sol.pop()
        
        #posso aggiungere 1 solo se la sua aggiunta non supera m
        if i==1 and m > 0:
            sol.append(i)
            es2r(n, m-1, k, sol)
            sol.pop()
            
        #posso aggiungere 2 solo se la sua aggiunta non supera k
        if i==2 and k > 0:
            sol.append(i)
            es2r(n, m, k-1, sol)
            sol.pop()

es2r(3, 1, 2)