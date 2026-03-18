import cv2

# load the image
img = cv2.imread('images/gerry.png')

# --- METODO 1: Grayscale "schifosa" (Fatta a mano con un ciclo FOR) ---

'''
Un primo metodo per convertire un'immagine a colori in scala di grigi è quello di prendere un solo canale (ad esempio 
il canale Blu) e copiarlo su tutti e tre i canali, per ottenere una combinazione (B, B, B).

Tuttavia questo metodo è estremamente inefficiente: In Python i cicli FOR sui pixel sono LENTISSIMI. 
Inoltre la scala di grigi non viene "omogenea" dal momento che il nostro occhio percepisce il verde 
molto più luminoso del blu... Dunque un'immagine basata solo sul blu sembrerà piu chiara di una solo verde.
'''

img_manual_B = img.copy()
img_manual_G = img.copy()
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        b, g, r = img[i][j]
        img_manual_B[i][j] = (b, b, b) 
        img_manual_G[i][j] = (g, g, g) 


# --- METODO 2: Grayscale "fatta bene" ---

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

'''
Usa la formula della LUMINOSITÀ PERCEPITA. Applica pesi diversi ai colori:
    Grigio = (0.299 * Rosso) + (0.587 * Verde) + (0.114 * Blu).
'''


# show the results
cv2.imshow('1 - Manual Blue', img_manual_B)
cv2.imshow('1 - Manual Green', img_manual_G)
cv2.imshow('2 - Grayscale', img_gray)
cv2.waitKey(0)


