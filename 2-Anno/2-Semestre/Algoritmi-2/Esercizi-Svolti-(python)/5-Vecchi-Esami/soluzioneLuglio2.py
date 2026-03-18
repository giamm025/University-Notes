# -*- coding: utf-8 -*-
"""
Created on Fri May 23 11:25:39 2025

@author: 39324
"""


def es2(n, sol = []):
    
    if len(sol)==n:
        print(''.join(sol))
        return
    
    rimasti = n-len(sol)
    for i in ['a', 'b', 'c']:
        
        #non posso mettere la 'a' quando non ho spazio per metterci due b dopo
        if i=='a' and rimasti>2:
            sol.append('a')
            sol.append('b')
            sol.append('b')
            es2(n, sol)
            sol.pop()
            sol.pop()
            sol.pop()
        
        #gli altri due simboli posso sempre metterli
        if i!='a':
            sol.append(i)
            es2(n, sol)
            sol.pop()

es2(4)