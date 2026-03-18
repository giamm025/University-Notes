import cv2
import numpy as np

'''
In questa lezione impareremo a disegnare forme geometriche su immagini in OpenCV. Prima di iniziare è fondamentale
ricordare che, come abbiamo gia visto in altri corsi di programmazione, l'origine (0,0) nelle immagini NON è in basso a sinistra
ma si trova in ALTO A SINISTRA:
    - L'asse X va verso DESTRA.
    - L'asse Y va verso il BASSO.
'''

# create a "black canvas" from scratch
# np.zeros is designed to create a matrix of any size filled with zeros.
img = np.zeros((300, 300, 3), dtype=np.uint8) 


'''
CIRCLE: cv2.circle()
    - img: image to draw on
    - center: tuple (x, y) indicating the center of the circle
    - radius: radius of the circle in pixels
    - color: tuple (B, G, R) indicating the color of the circle
    - thickness: thickness of the outline in pixels. If it is -1, the circle is filled.
'''
cv2.circle(img, (150, 150), 50, (0, 0, 255), thickness=-1) 
# thickness=-1 disegna un cerchio pieno, altrimenti disegnerebbe solo il contorno.

'''
RECTANGLE: cv2.rectangle()
    - img: image to draw on
    - top_left_point: tuple (x, y) indicating the top left corner
    - bottom_right_point: tuple (x, y) indicating the bottom right corner
    - color: tuple (B, G, R) indicating the color of the rectangle
    - thickness: thickness of the outline in pixels. If it is -1, the rectangle is filled.
'''
cv2.rectangle(img, (50, 50), (250, 250), (255, 0, 0), thickness=2) 
# thickness=2 disegna un contorno spesso 2 pixel.

'''
LINE: cv2.line()
    - img: image to draw on
    - start_point: tuple (x, y) indicating the starting point
    - end_point: tuple (x, y) indicating the ending point
    - color: tuple (B, G, R) indicating the color of the line
    - thickness: thickness of the line in pixels.
'''

cv2.line(img, (20, 20), (300, 300), (0, 255, 0), thickness=10) 
# in questo caso stiamo disegnando una linea diagonale (basta vedere i punti di inizio e fine).
# Inoltre, non ha senso usare thickness=-1 perche una linea non puo essere "riempita". Se lo facessimo, verrebbe disegnata 
# con spessore 1 pixel.


'''
TEXT: cv2.putText()
    - img: image to draw on
    - text: string indicating the text to write
    - bottom_left_point_of_text: tuple (x, y) indicating the bottom left point of the text
    - font: font type to use
    - scale: scale of the text
    - color: tuple (B, G, R) indicating the color of the text
    - thickness: thickness of the text in pixels.
'''
cv2.putText(img, "hello", (60, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)


'''
RISULTATI
'''

cv2.imshow('Geometry', img)
cv2.waitKey(0)
cv2.destroyAllWindows() 