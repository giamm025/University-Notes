import cv2

# load the image. The last 0 means that we want to read the image in grayscale
img = cv2.imread("./images/bridge.jpg", 0)  

'''1° DERIVATES: SOBEL OPERATOR '''
grad_x = cv2.Sobel(img, -1, 1, 0)  # derivate in X direction -> the final image will have only the VERTICAL edges
grad_y = cv2.Sobel(img, -1, 0, 1)  # derivate in Y direction -> the final image will have only the HORIZONTAL edges

'''
Parameters:
    - img: the input image
    - ddepth: the depth of the output image. It can be specific type (like cv2.CV_64F) or -1 to keep the same type as the input image.
    - dx: the order of the derivative in x direction. It can be 0, 1, or 2.
    - dy: the order of the derivative in y direction. It can be 0, 1, or 2.

Example: cv2.Sobel(img, -1, 1, 0) means "First derivative in the x direction and NO derivative in the y direction 
                                         The output image will have only the VERTICAL edges.
                                         Keep the same depth as the input image."

Note: In OpenCV, la "profondità" non c'entra nulla con il 3D. Indica il "Tipo di Dato" usato per memorizzare i pixel.
I principali tipi di profondità sono:
    - uint8 (cv2.CV_8U) : unsigned 8-bit integer (0 to 255)
    - int16 (cv2.CV_16S): signed 16-bit integer (-32768 to 32767)

Quando applichi il filtro di Sobel (che calcola una derivata matematica), cerchi la differenza di colore tra i pixel vicini:
    - Se passi dal nero (0) al bianco (255), la differenza è positiva (+255).
    - Se passi dal bianco (255) al nero (0), la differenza è negativa (-255)

Il problema è che il formato uint8 non accetta numeri negativi! Tutti i bordi che passano da chiaro a scuro (quindi con 
differenza NEGATIVA)verranno brutalmente tagliati a zero, diventando invisibili.

Per fare le cose fatte bene, non si usa -1... ma un formato che accetta i numeri negativi e i decimali, come cv2.CV_64F 
(numeri decimali a 64-bit). In questo modo il computer ricorda sia i bordi "positivi" che quelli "negativi".

Tuttavia, con queste profondità, ci ritroveremmo con un'immagine piena di pixel negativi (es. -200)... Ma il monitor di un PC
non sa come mostrare un pixel di colore "-200" (non esiste di fatti). Pertanto dobbiamo usare la funzione convertScaleAbs()
che prende i valori negativi, li converte in positivi (es. -200 diventa 200) e poi li scala in uuint8 per farli rientrare
nel range [0, 255]
'''

# we need to convert the result of the Sobel operator to an 8 bit image, otherwise we won't be able to display it
abs_x = cv2.convertScaleAbs(grad_x)  
abs_y = cv2.convertScaleAbs(grad_y) 
# nel nostro caso non è necessario, funzionerebbe anche senza... siccome abbiamo messo depth = -1, le derivate stanno
# utilizzando la stessa profondità dell'immagine originale (uint8) che il monitor è gia in grado di mostrare

''' 2° DERIVATES: LAPLACIAN OPERATOR '''
laplacian = cv2.Laplacian(img, -1, ksize=3)         # compute the second-order derivative of the image using the Laplacian operator. 
scaled_laplacian = cv2.convertScaleAbs(laplacian)   # like before, converta the Laplacian result to uint8 format for visualization.

'''
Parameters:
    - img: the input image
    - ddepth: the depth of the output image. Like before.
    - ksize: the size of the kernel to be used for the Laplacian operator. It must be a positive odd integer (1, 3, 5, etc.). 
             The default value is 1, which means that a 3x3 kernel will be used.

Confronto:
    - SOBEL (Derivata Prima): è come un'auto che calcola la pendenza della strada. Trova i bordi solo in una direzione per volta 
                              (infatti prima calcoliamo le linee verticali, poi quelle orizzontali e infine le uniamo).

    - LAPLACIAN (Derivata Seconda): è come un'auto che calcola l'accelerazione (il cambio di pendenza). Il grandissimo vantaggio è 
    che è omnidirezionale: trova tutti i bordi (orizzontali, verticali, diagonali) in un colpo solo, senza dover fare due separati.

Il GRANDE difetto di Laplacian è che essendo una derivata seconda, è estremamente sensibile. Se nella foto c'è un po' di "rumore" 
(un granello di polvere, un pixel leggermente più scuro, la sgranatura della fotocamera), il Laplacian urlerà: "ECCO UN BORDO!" e 
riempirà l'immagine di puntini bianchi fastidiosi. Sobel, invece, è molto più "morbido" e ignora queste imprecisioni.
'''

# combining the two images we'll get an image with all the edges, both vertical and horizontal. The edges will be brighter where the two images have brighter pixels in the same position
combined = cv2.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)  # combine the two images, both with 0.5 weight. The last 0 is a scalar added to each sum, we can use it to increase or decrease the brightness of the final image

# stampiamo le immagini
cv2.imshow("Originale", img)
cv2.imshow("Sobel x", abs_x)
cv2.imshow("Sobel y", abs_y)
cv2.imshow("Combined", combined)
cv2.imshow("Laplacian", scaled_laplacian)
cv2.waitKey(0)
cv2.destroyAllWindows()