# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 12:31:25 2025

@author: 39324
"""

def LCA(P, x, y, z):
    A = percorso(P, x)
    B = percorso(P, y)
    C = percorso(P, z)
    
    px, py, pz = A.pop(), B.pop(), C.pop()
    while px == py == pz:
        px, py, pz = A.pop(), B.pop(), C.pop()

def percorso(P, u):
    return

def trasforma(M):
    n = len(M)
    m = len(M[0])
    for i in range(n):
        for j in range(m):
            