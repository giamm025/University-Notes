import cv2
import numpy as np


# load the image
img = cv2.imread('./images/gerry.png')

'''
La proprietà .shape è fondamentale e restituisce una tupla con 3 valori:
    - img.shape[0]: Altezza (numero di righe di pixel, asse Y)
    - img.shape[1]: Larghezza (numero di colonne di pixel, asse X)
    - img.shape[2]: Numero di canali (3 per le immagini a colori, 1 per scala di grigi)
'''

# shape propriety: altezza, larghezza, canali
print(f"Dimensioni dell'immagine: \n\t(Altezza, Larghezza, Canali) = {img.shape}")
print(f"Dimensioni dell'immagine: \n\tAltezza: {img.shape[0]}\n\tLarghezza: {img.shape[1]}\n\tCanali: {img.shape[2]}")