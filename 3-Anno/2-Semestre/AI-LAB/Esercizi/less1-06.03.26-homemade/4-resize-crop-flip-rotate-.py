import cv2

# load the image
img = cv2.imread('./images/gerry.png')

# --- 1. RESIZE (Ridimensionamento) ---
'''
Possiamo utilizzare cv2.resize() per ridimensionare un'immagine. Tuttavia bisogna fare attenzione ai parametri...
Abbiamo gia visto in precedenza che img.shape restituisce in ordine:
    1. Altezza
    2. Larghezza
    3. Canali

Tuttavia cv2.resize() PRETENDE i parametri al contrario:
    1. Larghezza
    2. Altezza

Dunque una conversione tipo:
    cv2.resize(img, (img.shape[0]//5, img.shape[1]//5))

è un ERRORE che porta a un'immagine deformata e schiacciata, perché stiamo usando l'altezza come larghezza e viceversa.
'''

# ERRORE! Altezza e Larghezza invertite
img_bad_resize = cv2.resize(img, (img.shape[0]//5, img.shape[1]//5))

# GIUSTO: Bisogna passare prima Larghezza e poi Altezza
scale_factor = 0.5 
img_good_resize = cv2.resize(img, (img.shape[1]//5, img.shape[0]//5))

'''
Un altro modo di ridimensionare un'immagine è quello di specificare un fattore di scala (scale factor) per larghezza e altezza, 
invece di specificare le dimensioni esatte. In questo caso, si può passare None come secondo parametro e specificare fx e fy:
'''
scale_factor = 0.5  # Dimezziamo l'immagine
img_good_resize = cv2.resize(img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_AREA)

'''
Parameters:
    - img: l'immagine da ridimensionare
    - dsize: tupla (Larghezza, Altezza) che dice a OpenCV esattamente quanti pixel sarà grande l'immagine finale. 
    - fx: fattore di scala per la larghezza 
    - fy: fattore di scala per l'altezza
    - interpolation: metodo di interpolazione da usare per il ridimensionamento. 
                     INTER_AREA è spesso usato per ridurre le dimensioni, mentre INTER_LINEAR o INTER_CUBIC sono usati per ingrandire le immagini.
'''


# --- 2. CROP (Ritaglio) ---
'''
In OpenCV non esiste una funzione cv2.crop(). Poiché le immagini sono solo matrici Numpy, si usa lo "slicing" matematico:
                        img[y_inizio : y_fine , x_inizio : x_fine]
'''

# Ritaglia un quadrato dall'angolo in alto a sinistra (0,0) fino al pixel 300,300
cropped = img[0:300, 0:300]


# --- 3. FLIP (Specchio) ---
'''
Possiamo utilizzare la funzione diretta cv2.flip(img, flipCode). Dove flipCode è specifica il tipo di flip da eseguire:
    0  = Capovolge verticalmente (sottosopra)
    1  = Capovolge orizzontalmente (effetto specchio)
   -1  = Entrambe le cose contemporaneamente
'''
flipped = cv2.flip(img, 1)


# --- 4. ROTATE (Rotazione) ---
'''
Anche qui, esiste una funzione getRotationMatrix2D, ma dobbiamo seguire 2 passaggi:
    1. Creare una "Matrice di Rotazione" (getRotationMatrix2D)
    2. Applicare quella matrice all'immagine (warpAffine)
'''

# Calcolo dimensioni e centro immagine
(h, w) = img.shape[:2]             # Prendo altezza e larghezza
center = (w // 2, h // 2)          # Calcolo il centro esatto dell'immagine

# Ruotiamo l'immagine (nel nostro caso di 90 gradi in senso antiorario)
matrix = cv2.getRotationMatrix2D(center, 90, 1) 
rotated = cv2.warpAffine(img, matrix, (w, h))
# warpAffine applica matematicamente la rotazione

'''
Parameters getRotationMatrix2D:
    - center: punto attorno al quale ruotare (in questo caso il centro dell'immagine)
    - angle: angolo di rotazione in gradi (positivo per rotazione antioraria, negativo per oraria)
    - scale: fattore di scala (1 = nessuna scala, >1 ingrandisce, <1 riduce)

Parameters warpAffine:
    - img: immagine da ruotare
    - matrix: matrice di rotazione calcolata con getRotationMatrix2D
    - dsize: dimensione dell'immagine di output (in questo caso manteniamo le stesse dimensioni originali)

Nota: getRotationMatrix2D NON tocca minimamente l'immagine... modifica la matrice dell'immagine originale,
calcolando dove dovrà andare ogni pixel una volta ruotato. warpAffine, invece, prende la matrice (matrix) 
generata da getRotationMatrix2D e sposta fisicamente i pixel dell'immagine nella nuova posizione.

Il motivo per cui OpenCV ha deciso di separare questi due passaggi è l'EFFICIENZA. Se dovessimo ruotare un video 
a 60 fps, e la rotazione fosse un unico comando, il computer dovrebbe ricalcolare la matematica della rotazione 
60 volte al secondo. Separando i comandi, invece, si fa calcolare la matrice una volta sola, e poi si passa a warpAffine
dentro un ciclo ad altissima velocità per applicare le modifiche.
'''

cv2.imshow('1 - Resize Fatto Male', img_bad_resize)
cv2.imshow('1 - Resize Fatto Bene', img_good_resize)
cv2.imshow('2 - Cropped', cropped)
cv2.imshow('3 - Flipped', flipped)
cv2.imshow('4 - Rotated', rotated)

cv2.waitKey(0)
cv2.destroyAllWindows()