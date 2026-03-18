import cv2

img = cv2.imread('images/gerry.png')

'''
    HSV = Hue (Tonalità) + Saturation (Saturazione) + Value (Luminosità).

È potentissimo in Computer Vision perché separa il colore puro (Hue) dalla quantità di luce (Value). 
È utilissimo per riconoscere gli oggetti anche se c'è un'ombra sopra!

Quando converti in HSV, l'immagine rimane a 3 canali (esattamente come la BGR originale), ma Python cambia il "significato" 
dei tre numerini che compongono ogni pixel.

    - B diventa H (Hue - Tonalità):     Questo numero (che in OpenCV va da 0 a 179) indica solo ed esclusivamente il colore puro. Ad esempio: 0 è rosso, 60 è verde, 120 è blu.
    - G diventa S (Saturation):         Indica quanto è "acceso" o sbiadito il colore (da 0 a 255). Se è 0, il colore è un grigio spento; se è 255, è un colore fluo brillantissimo.
    - R diventa V (Value - Luminosità): Indica quanta luce c'è (da 0 a 255). Se è 0 è nero (buio totale), se è 255 è illuminato a giorno.

Nota: Quando usi cv2.imshow, OpenCV interpreta comunque l'immagine come BGR. Quindi prende il valore "Hue" e lo stampa a schermo 
come se fosse il colore Blu, creando un "effetto psichedelico". L'immagine HSV non è fatta per essere "guardata" da un umano, 
ma per essere analizzata matematicamente.
'''

img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.imshow('Original', img)
cv2.imshow('HSV', img_hsv)
cv2.waitKey(0)

'''
Esempio: Immagina di voler programmare un robot per raccogliere dei pomodori rossi. Se usi lo spazio colore standard (BGR/RGB), 
hai un problema gigantesco: le ombre. Un pomodoro colpito dal sole avrà i pixel RGB tipo: Rosso 255, Verde 50, Blu 50.
Lo stesso pomodoro, coperto dall'ombra, avrà i pixel tipo: Rosso 100, Verde 10, Blu 10.

Dunque, se scrivi un programma che cerca il numero "255" sul canale rosso, il robot non raccoglierà i pomodori all'ombra...
E qui entra in gioco la magia dell'HSV. In HSV, il colore (Hue) è separato dalla luce (Value):
    - Il pomodoro al sole avrà:     Hue = 0 (Rosso), Value = 255 (Tanta luce).
    - Il pomodoro all'ombra avrà:   Hue = 0 (Rosso), Value = 100 (Poca luce).

La Tonalità (Hue) è rimasta identica! Al computer basterà cercare i pixel con Hue = 0 e troverà tutti i pomodori, 
fregandosene totalmente se c'è il sole, se piove o se sono all'ombra.
'''