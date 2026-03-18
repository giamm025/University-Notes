# -*- coding: utf-8 -*-
"""
Created on Fri Mar 28 08:45:48 2025

@author: 39324
"""

#%% CONTARE ARCHI IN AVANTI, INDIETRO E DI ATTRAVERSAMENTO v. Rozza
def countArchi(G, u):
    n = len(G)
    visitati = [0]*n            #visitati[i] = 0: non visitat0; 1: visitando, 2: visita terminata
    tempo = [0]*n               #tempo[i] = numero dell'iterazione in cui ho scoperto il nodo i
    
    avanti = [0]              
    indietro = [0]             
    attraversamento = [0]        
    
    DFS(G, u, [0], visitati, tempo, avanti, indietro, attraversamento)   #gestebdo bene la ricorsione potremmo pensare che DFS
                                                                        #ritorna direttamente la terna (av, ind, att)
    return (avanti, indietro, attraversamento)

def DFS(G, u, t, visitati, tempo, avanti, indietro, attraversamento):
    visitati[u]=1
    tempo[u]=t[0]
    t[0]+=1
    for i in G[u]:
        
        if visitati[i]==1:
            indietro[0] += 1
        
        elif visitati[i]==2 and tempo[u]<tempo[i]:
            avanti[0] += 1
            
        elif visitati[i]==2 and tempo[u]>=tempo[i]:
            attraversamento[0] += 1
            
        elif visitati[i]==0:
            DFS(G, i, t, visitati, tempo, avanti, indietro, attraversamento)
    
    visitati[u]=2
    
G = [[1,2], [3], [3], [4,5], [5], [6], [1]]
print(countArchi(G, 0))

#%% CONTARE ARCHI IN AVANTI, INDIETRO E DI ATTRAVERSAMENTO v. Pulita
def countArchi(G, u):
    n = len(G)
    visitati = [0]*n            #visitati[i] = 0: non visitat0; 1: visitando, 2: visita terminata
    tempo = [0]*n               #tempo[i] = numero dell'iterazione in cui ho scoperto il nodo i      
    
    return DFS(G, u, [0], visitati, tempo)   


def DFS(G, u, t, visitati, tempo):
    visitati[u]=1
    tempo[u]=t[0]
    
    t[0]+= 1
    avanti = 0
    indietro = 0
    attraversamento = 0
    for i in G[u]:
        
        if visitati[i]==1:
            indietro += 1
        
        elif visitati[i]==2 and tempo[u]<tempo[i]:
            avanti += 1
            
        elif visitati[i]==2 and tempo[u]>=tempo[i]:
            attraversamento += 1
            
        elif visitati[i]==0:
            a, b, c = DFS(G, i, t, visitati, tempo)
            avanti           += a
            indietro         += b
            attraversamento  += c
    
    visitati[u]=2
    return avanti, indietro, attraversamento

G = [[1,2], [3], [3], [4,5], [5], [6], [1]]
print(countArchi(G, 0))