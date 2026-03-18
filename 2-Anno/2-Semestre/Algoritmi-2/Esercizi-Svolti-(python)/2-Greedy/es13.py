# -*- coding: utf-8 -*-
"""
Created on Thu May 15 12:31:09 2025

@author: 39324
"""

def es13a(A, B, C):
    n = len(A)
    m = len(B)
    
    a = 0
    b = 0
    for i in range(n+m):
        if C[i] == A[a]:
            a += 1
        elif C[i] == B[b]:
            b += 1
        else:
            return False
    
    return True



def es13b(A, B, C):
    n = len(A)
    m = len(B)
    
    