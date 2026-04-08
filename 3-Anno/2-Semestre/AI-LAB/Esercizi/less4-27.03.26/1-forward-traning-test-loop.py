import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
import torchmetrics

'''
1. PREPARE IL DATASET

Per prima cosa dobbiamo caricare il dataset da utilizzare per addestrare il modello.
In questo caso utilizziamo il dataset MNIST, che è come se fosse l' "Hello World" del Machine Learning. Contiene circa 70.000 immagini 
(28x28 pixel) di numeri scritti a mano, diviso in un set di addestramento e uno di test. 
'''

# Qui stiamo caricando il set di addestramento.
training_data = datasets.MNIST(
    root="./less4-27.03.26/data",       # directory in cui salvare il dataset
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
    root="./less4-27.03.26/data",           
    train=False,                    # specifica che vogliamo il set di test (NON addestramento come prima)
    download=True,                  
    transform=ToTensor()            
)

'''
2. CREARE I DATALOADER
'''
# usa 2 dataloaders (one for training, one for testing) to load the chunks of data from the dataset
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

    - __init__(self): definiamo la struttura del modello, ovvero quali tipi di layer utilizzeremo e come sono connessi tra loro.

    - forward(self, x): definiamo il flusso dei dati attraverso il modello, come i dati vengono trasformati dai layer per produrre l'output.
'''

class NeuralNetwork(torch.nn.Module):

    def __init__(self):
        super().__init__()                      # chiama il costruttore della superclasse (torch.nn.Module) per inizializzare il modello
        self.flatten = torch.nn.Flatten()       # 1. Flatten: è un layer necessario per i modelli LINEARI che "appiattisce l'immagine"
        self.layers = torch.nn.Sequential(      # 2. Sequential: definisce la sequenza di layer che compongono il modello
            
            # PRIMO LAYER
            # Prende in input i 784 pixel e li passa a 512 neuroni.
            torch.nn.Linear(28*28, 512),             
            torch.nn.ReLU(),                        
            
            # SECONDO LAYER
            # Prende in input i 512 segnali precedenti e li distilla in 64 neuroni.
            torch.nn.Linear(512, 64),
            torch.nn.ReLU(),

            # LAYER DI OUTPUT
            # Prende in input i 64 segnali e produce i 10 valori finali (logits) corrispondenti alle cifre 0-9.
            torch.nn.Linear(64, 10)                 
        )
    
    def forward(self, x):
        x = self.flatten(x)
        logits = self.layers(x)
        return logits
'''
Spiegazione:

    1. Flatten: Le reti neurali LINEARI vogliono i dati in fila indiana, non a griglia. Flatten prende 
       la griglia 28x28 e la "srotola" in una singola lista di 784 pixel.
            before flatten():  1....
            after flatten():   .....

    2. Layer "Linear" (La Matematica): È uno strato "completamente connesso". Prende dei dati in input, 
       li moltiplica per dei "Pesi" e somma un "Bias". L'equazione per ogni neurone è: y = (x * W) + b
        - Pesi (Weights, W): Una matrice di numeri decimali (aggiustati durante l'addestramento). Determinano 
          quanto un certo dato in ingresso è "importante" per far attivare quel neurone.
        - Bias (b): Un numero sommato alla fine. Determina la "severità" o la soglia di attivazione del neurone 
          (evita che si attivi troppo spesso o troppo raramente).

    3. Layer "ReLU" (Rectified Linear Unit): È la funzione di attivazione. Trasforma in 0 tutti i numeri 
       negativi e lascia intatti i positivi. 
       Perché lo usiamo? Mantenere solo i valori positivi fa concentrare la rete sulle "certezze". Inoltre, 
       senza ReLU la rete sarebbe solo una gigantesca moltiplicazione lineare e non potrebbe imparare pattern complessi.

    4. Il Flusso dei Dati (La Pipeline):
        - Primo strato: 784 pixel in ingresso -> 512 neuroni estraggono le prime caratteristiche generali + ReLU.
        - Secondo strato: I 512 segnali passano a 64 neuroni che estraggono concetti più complessi + ReLU.
        - Output (I Logits): I 64 segnali vengono compressi negli ultimi 10 neuroni. I 10 valori in uscita 
          rappresentano la probabilità (non ancora in percentuale) per ogni cifra da 0 a 9.
          
       NB: Sull'ultimo strato NON usiamo la ReLU! Questo perché nell'output finale vogliamo poter vedere anche i 
       numeri negativi. Se la rete è assolutamente certa che l'immagine NON sia un "4", potrebbe assegnargli un 
       punteggio di -50. Se mettessimo una ReLU alla fine, questo -50 verrebbe appiattito a 0, e perderemmo un
       informazione preziosissima!
    
    5. forward: Definisce come i dati fluiscono attraverso il modello. Nel nostro ccaso prima appiattiamo l'immagine, 
    con flatten, poi la passiamo attraverso i layer sequenziali, e infine restituiamo i logits (i 10 valori finali).
'''




'''
5. ISTANZIAZIONE & IPERPARAMETRI
'''
# Creiamo un'istanza fisica della nostra rete e la spostiamo sulla GPU (se disponibile)
model = NeuralNetwork().to(device)
print(model)                            # DEBUG

batch_size = 64
epochs = 2
learning_rate = 1e-3 # equivale a 0.001

'''
Gli iperparametri sono le "manopole" che noi impostiamo prima ancora che l'addestramento inizi:

    - batch_size: Quante immagini alla volta dare in pasto alla rete (es. 64). I computer e le schede video lavorano 
      meglio con le potenze del 2 (32, 64, 128, 256) per motivi di architettura hardware.
    
    - epochs (epoche): Quante volte la rete deve rileggere l'INTERO dataset da cima a fondo. Piu epoche, più la rete impara, 
      ma attenzione a non esagerare o rischiamo l'overfitting (la rete impara a memoria i dati di addestramento e non generalizza 
      bene sui dati nuovi).
    
    - learning_rate: È la grandezza del "passo" che la rete fa quando cerca di correggere i propri errori. Se è troppo piccolo, 
      ci metterà una vita a imparare. Se è troppo grande, salterà oltre la soluzione senza mai trovarla.
'''




'''
6. LOSS FUNCTION, L'OPTIMIZER E METRICHE DI VALUTAZIONE
'''
loss_fn = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
metric = torchmetrics.Accuracy(task='multiclass', num_classes=10).to(device)

'''
Loss Function e Optimizer lavorano in coppia per far imparare la rete (Backpropagation).

    - Loss Function (CrossEntropyLoss): È l'arbitro che guarda le risposte della rete e dice "Hai sbagliato di TOT". 
      La CrossEntropy trasforma i logits grezzi in probabilità (da 0 a 1) usando la funzione Softmax, e poi calcola 
      quanto siamo lontani dal risultato vero (usando il logaritmo negativo).
      
    - Optimizer (SGD - Stochastic Gradient Descent): È la bussola della rete. Prende l'errore calcolato dall'arbitro, 
      calcola il "gradiente" (la direzione in cui la pendenza dell'errore scende) e aggiorna i pesi per scendere a valle.
      Formula magica: Nuovo_Peso = Vecchio_Peso - (Gradiente * Learning_Rate)

Le metriche di valutazione (Accuracy) ci permettono di misurare quanto la rete stia effettivamente imparando, calcolando la 
percentuale di risposte corrette. Nel nostro caso usiamo:
    - torchmetrics per calcolare la percentuale di risposte corrette
    - Task="multiclass" perché stiamo classificando tra più etichette diverse (le 10 cifre).
'''



'''
7. TRAINING LOOP (Ciclo di Addestramento)
'''
def train_loop(train_dataloader, model, loss_fn, optimizer):

    data_size = len(train_dataloader)                   # calcola il numero totale di batch nel dataloader (quante volte dobbiamo ripetere il ciclo per vedere tutto il dataset)
    for batch, (x, y) in enumerate(train_dataloader):   # enumerate ci dà il numero del batch corrente, 'x' (immagini) e 'y' (etichette giuste)

        # 1. Spostiamo i dati sulla memoria della scheda video
        x = x.to(device)
        y = y.to(device)

        # 2. Forward Pass: Chiediamo alla rete di fare una previsione
        pred = model(x)
        
        # 3. Calcolo dell'Errore
        loss = loss_fn(pred, y)

        # 4. BACKPROPAGATION: La rete impara dai suoi errori
        loss.backward()         # Calcola le derivate (gradienti)
        optimizer.step()        # Applica i gradienti (aggiorna i pesi)
        optimizer.zero_grad()   # Pulisce la lavagna per il prossimo batch
        # ATTENZIONE! PyTorch di default SOMMA i gradienti vecchi a quelli nuovi. 
        # Se non azzeriamo la memoria dopo aver aggiornato i pesi, al giro successivo la rete mischierà le direzioni vecchie con quelle nuove e impazzirà!

        # Stampa i progressi ogni 100 batch per non inondare il terminale
        stampaDebug(batch, loss, pred, y)

    # A fine epoca calcoliamo l'accuratezza totale e resettiamo la metrica (necessario per evitare che accumuli i risultati di tutte le epoche)
    acc = metric.compute()
    print(f'\n---> Accuratezza Finale Epoca: {acc:.4f}\n')
    metric.reset()


def stampaDebug(batch, loss, pred, y):
    if batch % 100 == 0:
        loss_v = loss.item()
        print(f'Loss: {loss_v:.4f} | Batch attuale: {batch + 1}')

        acc = metric(pred, y)
        print(f'Accuratezza sul batch: {acc:.4f}')
'''
Questa è la vera e propria "palestra" della rete neurale.
Il ciclo si ripete per ogni batch. Le fasi fondamentali dentro il ciclo sono sempre 3:
   1) loss.backward(): Calcola di quanto abbiamo sbagliato (i gradienti) per ogni peso.
   2) optimizer.step(): Aggiorna materialmente i pesi per migliorare la volta successiva.
   3) optimizer.zero_grad():Cancella la memoria dell'errore. 
      FONDAMENTALE! altrimenti la rete ricorderebbe tutti gli errori passati e non riuscirebbe a imparare correttamente.
'''



'''
8. TEST LOOP (Ciclo di Valutazione)
Simile al training loop, ma con una grossa differenza: NON STIAMO IMPARANDO, STIAMO SOLO VERIFICANDO. 
Non ci serve aggiornare i pesi.
'''
def test_loop(test_dataloader, model):
    
    with torch.no_grad():   # FONDAMENTALE: spegne letteralmente la registrazione matematica dei gradienti. 
                            # Questo ci fa risparmiare un'enorme quantità di RAM e velocizza l'esecuzione.
                            # NECESSARIO in fase di test, altrimenti la rete continuerebbe a registrare i 
                            # gradienti e rischieremmo di esaurire la memoria della GPU.

        # per ogni coppia x=immagine e y=etichetta nel test_dataloader
        for x, y in test_dataloader:
            x = x.to(device)            # spostiamo le immagini sulla GPU  (se disponibile)
            y = y.to(device)            # spostiamo le etichette sulla GPU (se disponibile)

            pred = model(x)             # facciamo una previsione con la rete (chiediamo alla rete di valutare le immagini)
            acc = metric(pred, y)       # calcoliamo l'accuratezza del batch  (quante risposte corrette ha dato la rete)

        acc = metric.compute()  # calcoliamo l'accuratezza totale su tutto il set di test (necessario perché metric accumula i risultati di tutti i batch)
        print(f'*** ACCURATEZZA DI TEST FINALE: {acc:.4f} ***\n')   # DEBUG
        metric.reset()          # resettiamo la metrica per evitare che accumuli i risultati di tutte le epoche 
                                # (NECESSARIO per avere un risultato accurato alla fine di ogni epoca)


'''
9. ESECUZIONE
'''
for epoch in range(epochs):
    print(f'=============================')
    print(f' EPOCH: {epoch + 1}/{epochs}')
    print(f'=============================')
    
    train_loop(train_dataloader, model, loss_fn, optimizer)
    test_loop(test_dataloader, model)
    
print("Addestramento completato! 🎉")