# -*- coding: utf-8 -*-
"""
Created on Fri May 23 16:42:04 2025

@author: 39324
"""

def es2(n, sol = [], numUni1 = 0, numUni2 = 0):
    
    if len(sol)==(2*n):
        print(''.join(sol))
        return
    
    rimasti = (2*n) - len(sol)  
    #se sono nella prima metà posso mettere qualsiasi simbolo
    if len(sol) < n:
        for i in ['0', '1']:
            sol.append(i)
            if i=='1':
                es2(n, sol, numUni1+1)
            else:
                es2(n, sol, numUni1)
            sol.pop()
        
    #se sono nella seconda metà
    else:
        if numUni2 < numUni1:
            sol.append('1')
            es2(n, sol, numUni1, numUni2+1)
            sol.pop()
            
        if rimasti-1 >= numUni1 - numUni2:
            sol.append('0')
            es2(n, sol, numUni1, numUni2)
            sol.pop()
            
es2(2)



# def es2(n, sol = [], numUni1 = 0, numUni2 = 0):
    
#     if len(sol)==(2*n):
#         print(''.join(sol))
#         return
    
#     rimasti = (2*n) - len(sol)
#     for i in ['0', '1']:
        
#         #se sono nella prima metà
#         if len(sol) < n:
#             #posso mettere qualsiasi simbolo
#             sol.append(i)
#             if i=='1':
#                 es2(n, sol, numUni1+1)
#             else:
#                 es2(n, sol, numUni1)
#             sol.pop()
        
#         #se sono nella seconda metà
#         else:
#             if i=='1' and numUni2 < numUni1:
#                 sol.append(i)
#                 es2(n, sol, numUni1, numUni2+1)
#                 sol.pop()
                
#             elif i=='0' and (numUni1 == numUni2 or rimasti-1 >= numUni1 - numUni2):
#                 sol.append(i)
#                 es2(n, sol, numUni1, numUni2)
#                 sol.pop()

# es2(2)
          