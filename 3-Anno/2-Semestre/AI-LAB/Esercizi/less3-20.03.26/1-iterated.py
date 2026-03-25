import torch
from torch.utils.data import Dataset
from torchvision import datasets
import torch.utils.data as DataLoader
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt


training_data = datasets.MNIST(
    root="data",            # directory in cui salvare il dataset
    train=True,             # specifica che vogliamo il set di addestramento
    download=True,          # scarica il dataset se non è già presente
    transform=ToTensor()    # trasforma le immagini in tensori PyTorch
)

test_data = datasets.MNIST(
    root="data",            
    train=False,            # specifica che vogliamo il set di test (non addestramento come prima)
    download=True,         
    transform=ToTensor()    
)

batch_size = 64
train_dataloader = DataLoader.DataLoader(training_data, batch_size=batch_size)
test_dataloader = DataLoader.DataLoader(test_data, batch_size=batch_size)

for i in range(batch_size):
    imgs, labels = next(iter(train_dataloader)) # ottieni un batch di immagini e etichette dal DataLoader
    img = imgs[i]                               # prendi la prima immagine del batch (che è un tensore 3D con dimensioni [1, 28, 28], dove 1 è il numero di canali)
    img_squeezed = imgs[i].squeeze()            # rimuove la dimensione del canale (1, 28, 28) -> (28, 28)
    label = labels[i].item()

    print(f"Label: {label}")                 # stampa l'etichetta associata all'immagine visualizzata
    plt.imshow(img_squeezed, cmap="gray")    # visualizza l'immagine usando Matplotlib, specificando la mappa dei colori "gray" per visualizzare l'immagine in scala di grigi
    plt.show()                               # mostra la finestra con l'immagine