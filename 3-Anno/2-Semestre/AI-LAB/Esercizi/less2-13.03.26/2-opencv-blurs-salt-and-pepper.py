import cv2
import numpy as np

# load the image
img = cv2.imread("./images/lena.png")

'''
CONCETTO CHIAVE: COS'È UN KERNEL? (O Filtro)
Un kernel è semplicemente una piccola griglia di numeri (di solito 3x3 o 5x5) che OpenCV prende e fa "scivolare" 
sopra l'immagine originale, pixel per pixel. A ogni passo, moltiplica i colori dei pixel sotto la griglia per i 
numeri del kernel e li somma. Questo processo matematico si chiama CONVOLUZIONE.
'''

''' 1° CUSTOM KERNELS (Filtri personalizzati) '''

# Creiamo il nostro kernel personalizzato (una matrice 3x3)
my_kernel = np.array(
    [
        [1, 0, 1],
        [1, 0, 1],
        [1, 0, 1],
    ]
)
# In particolare questo kernel fa una somma dei pixel a destra e a sinistra, ignorando quello centrale (0).
# L'effetto visivo sarà ma una sorta di sfocatura direzionale o "sdoppiamento" orizzontale. 

# apply the kernel
filtered_img = cv2.filter2D(img, -1, my_kernel)


''' 2° AVERAGE BLUR (Sfocatura Media) '''

# Applichiamo una sfocatura molto forte all'immagine originale
blurred_img = cv2.blur(img, (30, 30))
less_blurred_img = cv2.blur(img, (10, 10))
# Il kernel di blur è un quadrato pieno di "1". La funzione blur() fa la media matematica di tutti i pixel in quel quadrato. 
# Per avere una sfocatura più leggera, basta usare un kernel più piccolo (es. 10x10 anzichè 30x30).

'''
Parameters di blur:
    - src: l'immagine di input
    - ksize: la dimensione del kernel (width, height). 

L'Average Blur è ottimo per nascondere i dettagli, ma pessimo se ci sono "rumori" estremi, perché li spalma ovunque.
'''


''' 3° GAUSSIAN BLUR (Sfocatura Gaussiana) '''

blurred_gaussian = cv2.GaussianBlur(img, (23, 23), 0)

#L'Average Blur dà la stessa importanza a tutti i pixel nel kernel, creando un effetto molto finto e "squadrato". 
# Il Gaussian Blur invece usa una curva a campana (la Gaussiana): dà tantissima importanza al pixel centrale e sempre 
# meno ai pixel lontani. Il risultato è una sfocatura molto più naturale, simile a quella dell'occhio umano o di una 
# lente fotografica fuori fuoco.

'''
Parameters GaussianBlur:
    - ksize: (23, 23). Deve essere dispari. Più è grande, più sfoca.
    - sigmaX: 0. È la deviazione standard sull'asse X. Mettendo 0, OpenCV la calcola
              da solo in base alla dimensione del kernel. È comodissimo!
'''


''' 4° MEDIAN BLUR (Sfocatura Mediana) '''

# Carichiamo un'immagine rovinata dal rumore "Sale e Pepe" (puntini neri e bianchi sparsi) ed utiliziamo il filtro 
# median blur per "curarla"
salty_img = cv2.imread('./images/salt_pepper.png') 
unsalty_img = cv2.medianBlur(salty_img, 3) 

# A differenza dell'Average Blur (che fa la media matematica), il Median Blur prende tutti i pixel sotto il suo kernel 3x3, 
# li mette in ordine di grandezza (dal più scuro al più chiaro) e sceglie esattamente quello IN MEZZO (la Mediana statistica).
# In questo modo i puntini neri (valore 0) e i puntini bianchi (valore 255) finiranno sempre agli ESTREMI della lista, mentre 
# la Mediana pescherà sempre un pixel "normale" dal centro della lista, facendo sparire il rumore.

'''
Parameters di medianBlur:
    - src: l'immagine rovinata di input
    - ksize: la dimensione del kernel. Deve essere un numero intero dispari (es. 3, 5, 7...). 

Il Median Blur è ottimo per rimuovere i "rumori" estremi (come il Sale e Pepe) senza sfocare troppo l'immagine, 
ma è più lento dell'Average Blur.
'''

''' 5° BILATERAL BLUR (Sfocatura Bilaterale) '''

blurred_bilateral = cv2.bilateralFilter(img, 25, 75, 75)

# Sia Gaussian che Median distruggono inesorabilmente i bordi degli oggetti (es. i contorni di un viso si fondono con lo sfondo).
# Bilateral Filter, invece, sfoca l'immagine MA CONSERVA I BORDI NETTI.

# Come fa? Usa DUE controlli contemporaneamente:
#    1. Controlla la distanza fisica (come il Gaussian).
#    2. Controlla la differenza di colore: se vede che c'è un salto netto di colore 
#       (es. tra la pelle e i capelli neri), blocca la sfocatura in quel punto! 
# Il risultato? La pelle diventa liscia come seta (rumore sparito), ma gli occhi e i contorni del viso rimangono nitidissimi.

'''
Parameters:
    - d: Il diametro dell'area dei pixel da controllare. Più è grande, più pixel vengono sfocati insieme.   Va da 1 a infinito. 
    - sigmaColor: Più è alto, più colori diversi verranno fusi insieme.                                     Va da 1 a infinito.
    - sigmaSpace: Più è alto, più i pixel lontani si influenzeranno a vicenda.                              Va da 1 a infinito.
'''

# salviamo l'immagine
cv2.imwrite('./images/unsalty_image.png', unsalty_img)   

# Mostriamo i risultati a schermo
cv2.imshow('1 - Custom Kernel', filtered_img)
cv2.imshow('2 - Blurred 30x30', blurred_img)
cv2.imshow('2 - Blurred 5x5', less_blurred_img)
cv2.imshow('3 - Gaussian Blur', blurred_gaussian)
cv2.imshow('4 - Median Blur - Salty', salty_img)
cv2.imshow('4 - Median Blur - Unsalty', unsalty_img)
cv2.imshow('5 - Bilateral Blur', blurred_bilateral)

cv2.waitKey(0)           # Aspetta all'infinito che tu prema un tasto
cv2.destroyAllWindows()  # Chiude tutte le finestre per non bloccare il computer