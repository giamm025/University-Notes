import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt

'''
1. PREPARE IL DATASET

Per prima cosa dobbiamo caricare il dataset da utilizzare per addestrare il modello.
In questo caso utilizziamo il dataset MNIST, che è come se fosse l' "Hello World" del Machine Learning. Contiene circa 70.000 immagini 
(28x28 pixel) di numeri scritti a mano, diviso in un set di addestramento e uno di test. 
'''

# Qui stiamo caricando il set di addestramento.
training_data = datasets.MNIST(
    root="./less3-20.03.26/data",       # directory in cui salvare il dataset
    train=True,                         # specifica che vogliamo il set di addestramento
    download=True,                      # scarica il dataset se non è già presente
    transform=ToTensor()                # trasforma le immagini in tensori PyTorch
)

'''
I  Tensori PyTorch sono simili agli array NumPy, ma possono essere utilizzati su GPU per accelerare i calcoli.
Nel dataset MNIST ogni immagine è rappresentata come un tensore 2D di dimensioni 28x28 pixel. La funzione ToTensor() normalizza 
automaticamente i valori dei pixel da [0, 255] a [0.0, 1.0], rendendo più facile l'addestramento dei modelli.
'''

# Qui stiamo caricando il set di test (che verrà utilizzato dopo l'addestramento per valutare le prestazioni del modello).
test_data = datasets.MNIST(
    root="./less3-20.03.26/data",           
    train=False,                    # specifica che vogliamo il set di test (NON addestramento come prima)
    download=True,                  
    transform=ToTensor()            
)

'''
2. CREARE I DATALOADER
'''

# use 2 dataloaders (one for training, one for testing) to load the chunks of data from the dataset
train_dataloader = DataLoader.DataLoader(training_data, batch_size=64)
test_dataloader = DataLoader.DataLoader(test_data, batch_size=64)

''' 
Un DataLoader è sostanzialmente un iteratore che consente di scorrere i dati in batch durante l'addestramento del modello.
Questi sono utili perché consentono di caricare i dati in modo efficiente, specialmente quando si lavora con grandi dataset 
che non possono essere caricati interamente in memoria.

Parameters:
    - dataset: il dataset da cui caricare i dati (in questo caso, training_data o test_data).
    - batch_size: il numero di campioni da caricare in ogni batch. Un batch più grande può accelerare l'addestramento, ma richiede più memoria.
    - shuffle: se True, i dati vengono mescolati ad ogni epoca (utile per evitare che il modello impari l'ordine dei dati).
    - num_workers: il numero di processi da utilizzare per caricare i dati. Un numero maggiore può accelerare il caricamento, ma richiede più risorse.
'''


'''
3. VISUALIZZARE UN'IMMAGINE E LA SUA ETICHETTA

Qui bisogna fare molta attenzione alla forma dei tensori e come questi siano DIVERSI rispetto alla rappresentazioni delle immagini
che abbiamo visto in precedenze. Attualmente abbiamo:
    - OpenCV:  (rows, cols, channels)
    - PyTroch: (batch_size, channels, rows, cols)

Questo significa che, in qualche modo, dobbiamo modificare la rappresentazione dei tensori per permettere di mostrarle con OpenCV/Matplotlib.
    
    - Per quanto riguarda la batch_size, questa sparisce automaticamente quando facciamo imgs[i], poiche andiamo a selezionare
      solo la foto che vogliamo visualizzare, non tutta la batch (e di conseguenza le immagini non hanno la propietà di batch_size).
    
    - Per quanto riguarda la dimensione dei canali, dovremmo spostarla dalla prima posizione (dove si trova in PyTorch) alla terza 
      posizione (dove si trova in OpenCV/Matplotlib). A tale scopo utilizzeremo la funzione permute() di PyTorch, che consente di 
      riorganizzare le dimensioni del tensore.

ATTENZIONE! nel caso delle immagini in scala di grigi (la dimensione dei canali è 1), possiamo semplicemente usare la funzione squeeze() 
che RIMUOVE la dimensione del canale, in quanto non necessaria per la visualizzazione. Tuttavia si ricorda che questo ragionamento vale
SOLO per le immagini in scala di grigi. Per immagini a colori (es. RGB) che usano 3 canali, DOBBIAMO utilizzare la funziona permute().
'''

imgs, labels = next(iter(train_dataloader)) # usiamo il dataloader per ottenere il prossimo batch di immagini con relative etichette
img = imgs[0]                               # prendi la prima immagine del batch, che è salvata come un tensore 3D con dimensioni (1, 28, 28), dove 1 è il numero di canali
img_squeezed = imgs[0].squeeze()            # "squeeze" rimuove la dimensione del canale (1, 28, 28) -> (28, 28)
label = labels[0].item()                    # prendi la prima etichetta del batch e converti da tensore a numero intero

print(f"Label: {label}")                    # stampa l'etichetta associata all'immagine visualizzata
plt.imshow(img_squeezed, cmap="gray")       # visualizza l'immagine usando Matplotlib, specificando la mappa dei colori "gray" per visualizzare l'immagine in scala di grigi
plt.show()                                  # mostra la finestra con l'immagine


'''
3.5 SELEZIONARE IL DISPOSITIVO PER L'ADDESTRAMENTO
'''
# get the device used for the training (GPU if available, otherwise CPU)
if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"

print(f"Using {device} device")


'''
4. DEFINZIONI DEL MODELLO (Rete Neurale)

I modelli sono come dei lego che possiamo assemblare per costruire architetture complesse. In PyTorch, definiamo un modello semplicemente
creando una classe che eredita da:
                                                torch.nn.Module
                                    
Questa classe fornisce tutte le funzionalità necessarie per costruire e addestrare un modello di machine learning personalizzato. 
Dovremo implementare due metodi principali:

    - __init__(self): definiamo l'hardware, cioe la struttura del modello, ovvero quali tipi di layer utilizzeremo e come sono connessi tra loro.

    - forward(self, x): definiamo il software, cioe il flusso dei dati attraverso il modello, come i dati vengono trasformati dai layer per produrre l'output.
'''

class NeuralNetwork(torch.nn.Module):

    def __init__(self):
        super().__init__()                  # chiama il costruttore della superclasse (torch.nn.Module) per inizializzare il modello

        self.flatten = torch.nn.Flatten()       # 1. Flatten: è un layer necessario per i modelli LINEARI che "appiattisce l'immagine"
        
        self.layers = torch.nn.Sequential(      # 2. Sequential: definisce la sequenza di layer che compongono il modello
            torch.nn.Linear(28*28, 32),             # il primo parametro dice quanti perceptron (neuroni) necessitiamo. siccome ogni pixel viene dato ad un perceptor diverso,
                                                    # avremi bisogno di un neurone per ogni pixel. basta stampare img.shape per scoprire quanti pixels ci sono nell'immagine

                                                    # il secondo parametro dice quanti neuroni vogliamo nel primo layer. 32 è un numero arbitrario che possiamo scegliere, 
                                                    # ma in generale più neuroni abbiamo, più complesso sarà il modello e più tempo ci vorrà per addestrarlo.
            
            torch.nn.ReLU(),                        # funzione di attivazione ReLU (Rectified Linear Unit) che introduce non linearità al modello

            torch.nn.Linear(32, 10)                 # secondo layer completamente connesso che prende come input il vettore di dimensione 32 prodotto dal primo layer, 
                                                    # e lo trasforma in un nuovo array di dimensione 10 (corrispondente alle 10 cifre da 0 a 9)
        )


    def forward(self, x):
        pass

'''
Spiegazione:

    1. Flatten: Le reti neurali LINEARI vogliono i dati in fila indiana, non a griglia. Flatten prende la griglia 28x28 e la "srotola" 
       in una singola lista di 784 pixel.
        
            before flattern()
            1....

            after flattern()
            .....

    2. Sequential: È il contenitore dei nostri layer. Definisce l'ordine (sequenziale) dei layer attraverso cui passeranno i dati.

        - Layer 1 (Linear): È uno strato "completamente connesso" (Dense/Fully Connected). Questo significa che TUTTI i 28x28 = 784 pixel 
          che formano l'immagine sono collegati a TUTTI i 32 neuroni. In particolare questo layer produce in output un vettore di 32 numeri, 
          che rappresentano le 32 caratteristiche che il modello ha imparato a riconoscere.

        - Layer 2 (ReLU): è un altro layer completamente connesso che prende in input i 32 output del primo layer e produce un output di
          dimensione 10, corrispondente alle 10 classi di cifre da 0 a 9. La funzione di attivazione viene applicata ai 32 numeri in 
          uscita dal primo strato. Lascia intatti i positivi e azzera i negativi.

        - Layer 3 (Linear Output): Prende in input i 32 valori passati dalla ReLU e li comprime in 10 valori finali. 
          Il valore più alto tra questi 10 indicherà quale cifra (da 0 a 9) la rete pensa di aver "visto".
'''