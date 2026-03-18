import cv2
import numpy as np

'''
Lo scopo di questa lezione è capire come funzionano i canali di colore in OpenCV e come possiamo dividerli e manipolarli.
Il primo tranello fondamentale è che OpenCV, a differenza di quasi tutti gli altri programmi al mondo, legge le immagini 
a colori nel formato BGR (Blue, Green, Red), anziche RGB (Red, Green, Blue). Questo è un retaggio storico dovuto a motivi 
di efficienza.

Tuttavia, a causa di questo problema, in alcuni casi potrebbe essere necessario convertire l'immagine da BGR a RGB, o viceversa.
Per farlo si utilizza il comando cv2.cvtColor().
'''

# load the image
img = cv2.imread('./images/gerry.png')

# convert BGR to RGB
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


'''
METODO 1: IL METODO "INTUITIVO"
'''

# Creiamo una copia per non rovinare l'immagine originale
img_green_loop = img.copy()

for i in range(0, img_green_loop.shape[0]):       # Scorriamo l'altezza (Asse Y)
    for j in range(0, img_green_loop.shape[1]):   # Scorriamo la larghezza (Asse X)
        
        # Estraiamo i 3 valori del pixel corrente. 
        # OCHO: in OpenCV l'ordine è sempre BGR, non RGB!
        (b, g, r) = img_green_loop[i, j] 
        
        # Sovrascriviamo il pixel spegnendo il Blu (0) e il Rosso (0), 
        # lasciando intatto solo il valore originale del Verde (g).
        img_green_loop[i, j] = (0, g, 0)


# Usiamo i cicli FOR per scorrere ogni singolo pixel... nella pratica questo metodo è INEFFICIENTE e LENTISSIMO. 
# Su un'immagine grande, questo blocco potrebbe impiegare svariati secondi.

'''
METODO 2: IL METODO "PROFESSIONALE"

Usiamo le funzioni native di OpenCV e NumPy (scritte in C++ dietro le quinte). Questo metodo elabora milioni di pixel 
in una frazione di millisecondo.
'''

# Separiamo i canali di colore usando cv2.split().
b, g, r = cv2.split(img)    # Otteniamo 3 matrici separate, una per ogni canale.

# Creiamo una "tela nera" (piena di zeri) grande esattamente quanto uno dei canali.
# Ci servirà per "spegnere" i colori che non vogliamo vedere.
zeros = np.zeros_like(b)
# Usiamo np.zeros_like() poiche ci permette di creare una matrice di zeri con le stesse dimensioni di 'b', direttamente,
# senza vedere a mano le dimensioni e dirgli "creami una matrice di 800x600 con tutti (0, 0, 0)".

# A questo punto, tramite la funzione merge(), possiamo ricostruire l'immagine, mantenendo solo il canale che ci interessa.
blue_img =  cv2.merge([b, zeros, zeros])   
green_img = cv2.merge([zeros, g, zeros])
red_img =   cv2.merge([zeros, zeros, r])

'''
RISULTATI
'''

# show the results
cv2.imshow('Originale', img)
cv2.imshow('Convertita RGB', img_rgb)

cv2.waitKey(0)                  
cv2.destroyAllWindows()

# Mostriamo il risultato del ciclo FOR (lento)
cv2.imshow('Green (Fatto col ciclo FOR)', img_green_loop)

cv2.waitKey(0)                  
cv2.destroyAllWindows()

# Mostriamo i risultati del metodo Split/Merge (veloce)
cv2.imshow('Blue Channel Only', blue_img)
cv2.imshow('Green Channel Only', green_img)
cv2.imshow('Red Channel Only', red_img)

cv2.waitKey(0)                  # esprime quanto tempo (in millisecondi) la finestra rimane aperta. 0 = finche non premi un tasto
cv2.destroyAllWindows()         # Chiude tutte le finestre per non bloccare il computer