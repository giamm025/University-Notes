# -*- coding: utf-8 -*-
"""
Created on Thu May 15 17:50:07 2025

@author: 39324
"""
       
def kermit(Q):
    n = len(Q)
    T = [[False for _ in range(n)] for _ in range(n)]
    T[0][1] = True
    
    for i in range(1, n):
                    
        if Q[i] == 0:
            continue
        
        for j in range(1, n):
            
            if (j > 1 and T[i-j][j-1]) or (i-j > 0 and T[i-j][j]) or (j < n-1 and T[i-j][j+1]):
                T[i][j] = True
    
    stampaMatrice(T)
    
    for j in range(n):
        if T[n-1][j] == True: 
            print(kermitBT(T, i, j))
            return True
    
    return False



def stampaMatrice(M):
    n = len(M)
    for i in range(n):
        print(M[i])

def kermitBT(T, i, j):
    n = len(T)
    path = []
    while i > 0:
        path.append(j)
        prev = i - j
        for kp in (j-1, j, j+1):
            if 1 <= kp < n and prev >= 0 and T[prev][kp]:
                j = kp
                i = prev
                break
            
    # aggiungiamo il salto iniziale
    path.append(1)
    path.reverse()
    return path
    

Q = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1]
print(kermit(Q))

print()

Q = [1, 0, 1, 1, 0, 1]
print(kermit(Q))