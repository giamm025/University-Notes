# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 09:34:22 2025

@author: 39324
"""
#%% VISITA DFS RICORSIVA
def DFS(G, u):
    n = len(G)
    visitati = [0]*n
    DFSr(G, u, visitati)
    return [x for x in range(n) if visitati[x]==1]

def DFSr(G, u, visitati):
    visitati[u]=1 
    for i in G[u]:
        if visitati[i]==0:
            visitati[i]=1
            DFSr(G, i, visitati)

# VISITA DFS ITERATIVA
def DFSi(G, u):
    n = len(G)
    visitati = [0]*n
    visitati[u] = 1
    
    pila = [u]
    while pila:
        u = pila.pop()
        for i in G[u]:
            if visitati[i]==0:
                visitati[i] = 1
                pila.append(i)
    
    return [x for x in range(n) if visitati[x]==1]
 


#%% VETTORE DEI PADRI RICORSIVO
def Padri(G, u):
    n = len(G)
    padre = [-1]*n
    padri2(G, u, u, padre)
    return padre

def padri2(G, u, p, padre):
    padre[u] = p
    for y in G[u]:
        if padre[y]==-1:
            padri2(G, y, u, padre)

# VETTORE DEI PADRI ITERATIVO
def PadriI(G, u):
    n = len(G)
    padre = [-1]*n
    padre[u] = u
    
    pila = [u]
    while pila:
        v = pila.pop()
        for i in G[v]:
            if padre[i]==-1:
                padre[i] = v
                pila.append(i)

    return padre
 
    
#%% TROVARE IL POZZO UNIVERSALE v. ITERATIVA
def findPozzoUniversale(G):
    n = len(G)               #numero di nodi
    pozzo = [];
    for x in range(n):
        if G[x].isEmpty():   #x non ha archi uscenti.
            pozzo.append(x)  #quindi x è un pozzo
    
    if len(pozzo) == 1:      #se ho più di un pozzo NON puo   
        x = pozzo[0]         #esserci un pozzo universale
        for y in range(n):
            if x not in G[y]: 
                return None
        return x
 
    
#%% TROVARE UN CAMMINO v. ITERATIVA
def camminoI(G, x, y):
    albero = Padri(G, x)            #calcolo l'albero DFS. Costo O(n+m)
    cammino = []
    if albero[y] == -1: return []   #se mio padre è -1 non sono raggiungibile da x
    
    while albero[y] != x:           #risalgo l'albero finchè non arrivo alla radice. Costo O(n)
        cammino.append(y)           #inserisco tutti i nodi che attraverso in una lista. Uso append perche costa O(1)
        y = albero[y]               
    cammino.append(x)               #alla fine inserisco anche la radice
    cammino.reverse()               #rigiro la lista per restituire l'ordinamento corretto. Costo O(n)
    
    return cammino


# TROVARE UN CAMMINO v. RICORSIVA
def cammino(G, x, y):
    padre = Padri(G, x)                 #ottengo il vettore dei padri
    cammino = []
    if padre[y] != -1:                  #se y non ha padre significa che NON è raggiungibile da x
        camminoR(padre, y, cammino)
        cammino.reverse()               #siccome parto da y e risalgo mano mano l'albero, alla fine avro il cammino
                                        #salvato come y <-... <-x. Invece vogliamo x-> ...-> y
    return cammino

def camminoR(padre, y, cammino):
    if padre[y]==y:                #quando sono alla radice termino
        return
                     
    cammino.append(y)              #aggiungo me stesso subito dopo mio padre
    camminoR(padre, padre[y], cammino)    #eseguo di nuovo
        

#%% TRASPORRE UN GRAFO (invertire i nodi)
def trasponi(G):
    n = len(G)
    GT = [[] for _ in range(n)]
    for u in range(n):
        for i in G[u]:
            GT[i].append(u)

    return GT

#%% BI-COLORA UN GRAFO assumendo che sia già senza cicli dispari
def bicolora(G):
    n = len(G)
    colore = [-1]*n
    coloraNodo(G, 0, 0, colore)
    
    visitati = [0]*n
    if not èBicolorabile(G, 0, colore, visitati): 
        return "Impossibile bicolorare. Il grafo ha un ciclo dispari"
    
    return colore

def coloraNodo(G, u, c, colore):
    colore[u] = c
    for i in G[u]:
        if colore[i] == -1:
            coloraNodo(G, i, 1-c, colore)
            

def èBicolorabile(G, u, colore, visitati):
    visitati[u]=1
    for i in G[u]:
        if colore[u] == colore[i]:
            return False
        
        if visitati[i]==0:                                  #se ancora non l'ho visitato
            if not èBicolorabile(G, i, colore, visitati):   #lo visito e controllo: Se sotto di me NON è colorabile...
                return False                                #...allora l'intero grafo non lo è
        
    return True     #se arrivo qui significa che nessun nodo ha trovato un figlio con il suo stesso colore => è bicolorabile
    

G = [[1], [2], [0]]
print("Il grafo ", G, " bicolorato diventa:\n", bicolora(G), "\n")

G = [[1], [2], [3], []]
print("Il grafo ", G, " bicolorato diventa:\n", bicolora(G), "\n")

#%% TROVARE UN ORDINAMENTO TOPOLOGICO
def sortTop(G):
    n = len(G)
    gradoEnt = [0]*n
    for u in range(n):
        for i in G[u]:
            gradoEnt[i] += 1
    
    sort = []
    sorgenti = [x for x in range(n) if gradoEnt[x]==0]
    while sorgenti:
        u = sorgenti.pop()
        sort.append(u)
        for i in G[u]:
            gradoEnt[i] -= 1
            if gradoEnt[i]==0:
                sorgenti.append(i)
    
    if len(sort)==len(G): return sort
    return "Impossibile, il grafo presenta un ciclo"

G = [[1], [2], [0]]
print("Un sort topologico è:\n", sortTop(G), "\n")

G = [[1], [2, 3, 4], [], [5], [], [4]]
print("Un sort topologico è:\n", sortTop(G), "\n")

#%% TROVARE CICLI IN UN GRAFO DIRETTO
def findCiclo(G):
    n = len(G)
    visitati=[0]*n
    return DFS(G, 0, visitati)
    
    
def DFS(G, u, visitati):
    visitati[u]=1
    for i in G[u]:
        
        if visitati[i]==1:  #in questo caso ho un arco all'indietro (e quindi un ciclo) poiche sto
            return True     #visitando un nodo che ha ancora la ricorsione attiva (e quindi è mio antenato)
        
        if visitati[i]==0:          #se non l'ho ancora visitato vado ad esplorarlo per vedere se ha un ciclo
            if DFS(G, i, visitati): #ritorno il risultato della visita ai miei figli. 
                return True         
    
    #NON faccio direttamente return DFS(...) perche altrimenti ritorneremmo subito anche false, senza visitare gli altri archi in G[u]
    #nel caso in cui abbiamo un True invece non serve andare avanti nelle visite. Basta trovare un ciclo per terminare.
    
    visitati[u]=2
    return False

G = [[1, 2], [2], []]
print(findCiclo(G))

#%% TROVARE CICLI IN UN GRAFO INDIRETTO
def findCiclo(G):
    n = len(G)
    visitati = [0]*n
    return DFS(G, 0, 0, visitati)

def DFS(G, u, p, visitati):
    visitati[u]=1
    for i in G[u]:
        if visitati[i]==1 and i!=p:
            return True
        
        if visitati == 0:
            if DFS(G, i, u, visitati):
                return True
    
    return False



#%% RENDERE UN GRAFO DIRETTO UN DAG
def rendiDAG(G):
    n = len(G)
    visitati = [0]*n
    DAG = [[] for _ in range(n)]
    DFS(G, 0, visitati, DAG)
    return DAG

def DFS(G, u, visitati, DAG):
    visitati[u]=1
    for i in G[u]:

        if visitati[i]==1:
            DAG[i].append(u)    #ho un arco all'indietro (che genera un ciclo).
                                #quindi gli cambio la direzione dell'arco
        else:
            DAG[u].append(i)    #altrimenti copio l'arco così com'è perche non crea problemi
        
        if visitati[i]==0:
            DFS(G, i, visitati, DAG)

    visitati[u]=2


def findCiclo(G):
    n = len(G)
    visitati=[0]*n
    return DFSu(G, 0, visitati) 
def DFSu(G, u, visitati):
    visitati[u]=1
    for i in G[u]:
        
        if visitati[i]==1:  #in questo caso ho un arco all'indietro (e quindi un ciclo) poiche sto
            return True     #visitando un nodo che ha ancora la ricorsione attiva (e quindi è mio antenato)
        
        if visitati[i]==0:          #se non l'ho ancora visitato vado ad esplorarlo per vedere se ha un ciclo
            if DFSu(G, i, visitati): #ritorno il risultato della visita ai miei figli. 
                return True         
    
    #NON faccio direttamente return DFS(...) perche altrimenti ritorneremmo subito anche false, senza visitare gli altri archi in G[u]
    #nel caso in cui abbiamo un True invece non serve andare avanti nelle visite. Basta trovare un ciclo per terminare.
    
    visitati[u]=2
    return False
    

G = [[1], [2], [0]]
print("G ha un ciclo? ", findCiclo(G))
DAG = rendiDAG(G)
print("Trasformato in DAG diventa: ", DAG)
print("Adesso G ha un ciclo? ", findCiclo(DAG))

print("\n")

#%% PRENDE UN GRAFO INDIRETTO COMPLETO E DECIDE COME ORIENTARE GLI ARCHI PER RENDERLO UN DAG
def rendiDAG(G):
    n = len(G)
    visitati = [0]*n
    DAG = [[] for _ in range(n)]
    DFS(G, 0, visitati, DAG)
    return DAG

def DFS(G, u, visitati, DAG):
    visitati[u]=1
    for i in G[u]:
        if visitati[i]!=1:
            DAG[u].append(i)
            
        if visitati[i]==0:
            DFS(G, i, visitati, DAG)
    
    visitati[u]=2

        
G = [[1, 2, 3], [0, 2, 3], [0, 1, 3], [0, 1, 2]]
DAG = rendiDAG(G)
print("Trasformato in DAG diventa: ", DAG)
print("Adesso G ha un ciclo? ", findCiclo(DAG))

print("\n")


#%% ATTRAVERSARE TUTTI GLI ARCHI UNA SOLA VOLTA (in entrambe le direzioni )

#Visito tutti gli archi in una sola direzione. Alla fine della ricorsione, tramite i return, li visiterò anche nell'altra.
#Per garantire che l'arco venga attraversato una sola volta lo cancello dalla lista di adiacenza di entrambi i nodi (sia il
#padre/chiamante che il figlio/chiamato). Tuttavia la cancellazione in una lista costa O(n) quindi tocca fare canc. logica 💀
def visitaArchi(G):
    percorso = []
    DFSstrana(G, 0, 0, percorso)
    return percorso
    
def DFSstrana(G, u, p, percorso):
    percorso.append(u)
    m = len(G[u])
    for i in range(m):
        if G[u][i] == p:        #cerco l'arco che punta a mio padre
            G[u][i] = -1        #e lo cancello logicamente. Cosi non lo visito di nuovo
    
    
    for j in range(m):
        v = G[u][j]                         #v è il nodo che voglio raggiungere
        if v != -1:                         #se non ho gia attraversato questo arco
            G[u][j] = -1                    #lo segno come attraversato
            DFSstrana(G, v, u, percorso)    #e poi lo attraverso
      
    #quando l'ultimo nodo NON avrà piu nodi da visitare i vari return mi
    #permetteranno di ripercorrere il cammino al contrario, visitando ciascun
    #arco anche nell'altra direzione


G = [[1], [0, 2, 3, 4], [1, 3], [1, 2, 4], [1, 3]]
print("Il percorso in avanti è: ", visitaArchi(G))

#%% CONTARE LE COMPONENTI CONNESSE CHE SONO ANCHE ALBERI v. Inutilmente Lunga

#calcola il vettore delle compoenneti. Per ciascun nodo controllo: Se fa parte
#di una componenete che ancora non ho visitato la visito e controllo se è un
#albero. Altrimenti vado alla componenete successiva
def contaAlberi(G):
    n = len(G) 
    count = 0
    
    comp = vettComp(G)         #prendo il vettore delle componenti di G
    c = 1                      #i mi dice quale componente sto verificando
    for u in range(n):      
        if comp[u] == c:        #prendo un nodo di quella componente
            visitati = [0]*n
            if èAlbero(G, u, u, visitati):   #e controllo se è un albero
                count += 1
            c += 1              #passo alla componente successiva
    
    return count



#un albero è un grafo connesso aciclico. Tuttavia, siccome sto lavorando con 
#la componente connessa di u è sufficiente verificare che tale componente sia 
#anche aciclica per dire che è un albero. 
def èAlbero(G, u, p, visitati):  
    visitati[u]=1
    for i in G[u]:
        if i != p and visitati[i]==1:
            return False
        
        if visitati[i]==0:
            if èAlbero(G, i, u, visitati):
                return False
        
    visitati[u]=2
    return True



def vettComp(G):
    n = len(G)
    comp = [-1]*n
    c = 1
    for u in range(n):
        if comp[u] == -1:
            DFS(G, u, c, comp)
            c += 1
   
    return comp

def DFS(G, u, c, comp):
    comp[u]=c
    for i in G[u]:
        if comp[i] == -1:
            DFS(G, i, c, comp)
    
    
    
G = [[2], [2], [0, 1], [], [], []]
print("Le componenti sono: ", vettComp(G))
print("Il numero di componenti che sono anche alberi sono: ", contaAlberi(G))


#%% CONTARE LE COMPONENTI CONNESSE CHE SONO ANCHE ALBERI v. Migliorata

#NON ci interessa sapere di quale componente fa parte x. Ci basta sapere che 
#tale componente (cioè l'insieme dei nodi raggiungibili da x) sia aciclica.
#In tal caso la componente è un albero, in caso contrario no.
def contaAlberi(G):
    n = len(G)
    count = 0
    visitati = [0]*n
    for u in range(n):
        if visitati[u] == 0:
            count += èAlbero(G, u, u, visitati)

    return count

def èAlbero(G, u, p, visitati):  
    visitati[u]=1
    for i in G[u]:
        
        if i != p and visitati[i]==1:
            return False
        
        if visitati[i]==0:
            if èAlbero(G, i, u, visitati):
                return False
        
    visitati[u]=2
    return True
    
    
G = [[1, 2], [0, 2], [0, 1], [], []]
print("Le componenti sono: ", contaAlberi(G))

#%% CONTARE I POZZI RAGGIUNGIBILI DA UN CERTO NODO u
def contaPozzi(G, u):
    n = len(G)
    visitati = [0]*n
    return DFSp(G, u, visitati)


def DFSp(G, u, visitati):
    visitati[u]=1
    
    archiUscenti = len(G[u])
    if archiUscenti == 0:
        return 1
    
    count = 0
    for i in G[u]:
        if visitati[i]==0:
            count += DFSp(G, i, visitati)
    
    return count

G = [[], [0, 2, 3, 4, 5], [], [], [], []]
print(contaPozzi(G, 1))


