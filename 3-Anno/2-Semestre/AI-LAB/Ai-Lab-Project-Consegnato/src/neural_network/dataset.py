import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import torch
import numpy as np
from torch.utils.data import Dataset, Subset
from config import PROCESSED_DIR, LABEL_MAP


class SignLanguageDataset(Dataset):

    # costruttore del Dataset: prepara la lista dei file, delle etichette e calcola il padding
    def __init__(self, data_dir, exclude_augmented=False):

        self.data_dir = data_dir  # il percorso alla cartella in cui abbiamo salvato i file .npy contenenti le coordinate delle mani di ogni video (nel nostro caso PROCESSED_DIR)
        self.exclude_augmented = exclude_augmented # FLAG CRITICO: Se True, ignora i file generati dall'augmentation
        self.filenames = (
            []
        )  # conterrà la lista dei file .npy contenenti le coordinate delle mani di ogni video
        self.labels = (
            []
        )  # conterrà la lista delle soluzioni. questo array è parallelo a filenames (es. se filenames[0] è "hello_12345.npy" allora labels[0] conterrà "0" che tradotto significa "hello")
        self.max_frames = 0  # conterrà il numero di frame del video più lungo. ci servira per fare il PADDING

        # per ogni file .npy nella cartella data_dire (nel nostro caso PROCESSED_DIR)
        for filename in os.listdir(data_dir):

            # se NON è un file .npy lo saltiamo
            if filename.endswith(".npy"):
                # saltiamo i file che contengono '_aug_' nel nome (lo useremo in fase di test per evitare di testare il modello su video uguali a quelli di train... ma semplicemente con le mani scambiate)
                if self.exclude_augmented and "_aug_" in filename:
                    continue

                # estriamo la singola parole (poiche ogni filename è tipo "hello_12345.npy" possiamo splittare su '_')
                word = filename.split("_")[0]
                if word in LABEL_MAP:
                    self.filenames.append(
                        filename
                    )  # salviamo il filename (es. "hello_12345.npy") nella lista dei file
                    self.labels.append(
                        LABEL_MAP[word]
                    )  # salviamo la relativa soluzione (es. "0" per "hello")

        # calcoliamo il numero di frame del video più lungo (ci serve per fare il padding)
        self.calculate_max_frames(self.filenames, self.data_dir)

    # funzione per calcolare dinamicamente il numero di frame del video piu lungo (ci serve per il padding)
    def calculate_max_frames(self, filenames, data_dir):
        print("Calcolo la lunghezza massima dei video per il padding...")

        for filename in filenames:
            filepath = os.path.join(data_dir, filename)
            data = np.load(filepath)
            if data.shape[0] > self.max_frames:
                self.max_frames = data.shape[0]

        print(
            f"-> Il video più lungo dura {self.max_frames} frame. Uso questo valore per il padding di tutti i video!"
        )

    # getter per sapere sempre quanti video abbiamo in totale (es. 100 video di "hello", 80 video di "book", ecc.)
    def __len__(self):
        return len(self.filenames)

    # getter per ottenere un video specifico a partire dall'indice
    def __getitem__(self, idx):

        # prende il filename e costruisce il filepath
        filename = self.filenames[idx]
        filepath = os.path.join(self.data_dir, filename)

        # estrae l'etichetta corrispondente a questo video (es. 0 per "hello", 1 per "book", ecc.)
        label = self.labels[idx]

        # estrae i keypoints dal file .npy
        data = np.load(filepath)

        # salviamo la lunghezza REALE del video prima di aggiungere il padding
        # ci servirà per dire alla LSTM dove finisce il video vero e iniziano gli zeri
        real_len = data.shape[0]

        # --------------------------------------------------- PADDING ---------------------------------------------------
        seq_len = data.shape[0]
        padding = np.zeros(
            (self.max_frames - seq_len, data.shape[1])
        )  # crea matrici di zeri per i frame mancanti
        data = np.vstack(
            (data, padding)
        )  # aggiunge gli zeri alla fine dei dati originali
        # ---------------------------------------------------------------------------------------------------------------

        # converte gli array NumPy in Tensori PyTorch
        data_tensor = torch.tensor(data, dtype=torch.float32)
        label_tensor = torch.tensor(label, dtype=torch.long)
        length_tensor = torch.tensor(real_len, dtype=torch.long)

        return data_tensor, label_tensor, length_tensor

"""
Carica i dati da una cartella specifica, esegue lo split garantendo che ci sia lo stesso numero di video per ogni parola 
nei tre set (train, val, test) e applica l'augmentation SOLO al set di training.

Ritorna: (train_dataset, val_dataset, test_dataset) grezzi.
"""
def get_stratified_dataset_splits(data_dir, seed):

    # carichiamo l'intero dataset originale (SENZA augmentation) 
    base_dataset = SignLanguageDataset(data_dir, exclude_augmented=True)
    split_generator = torch.Generator().manual_seed(seed)

    # raggruppiamo le parole uguali
    label_to_indices = {}
    for idx, label in enumerate(base_dataset.labels):
        if label not in label_to_indices:
            label_to_indices[label] = []
        label_to_indices[label].append(idx)

    train_indices = []
    val_indices = []
    test_indices = []

    # applichiamo lo split stratificato
    for label, idxs in label_to_indices.items():
        idxs_tensor = torch.tensor(idxs)
        shuffled_idxs = idxs_tensor[torch.randperm(len(idxs_tensor), generator=split_generator)].tolist()
        
        n = len(shuffled_idxs)
        n_train = int(0.65 * n)
        n_val = int(0.15 * n)
        
        train_indices.extend(shuffled_idxs[:n_train])
        val_indices.extend(shuffled_idxs[n_train:n_train + n_val])
        test_indices.extend(shuffled_idxs[n_train + n_val:])

    # creiamo i sotto-dataset (Subsets) usando gli indici stratificati (che garantiscono lo stesso numero di video per ogni parola in ogni set)
    training_base = Subset(base_dataset, train_indices)
    val_data      = Subset(base_dataset, val_indices)
    test_data     = Subset(base_dataset, test_indices)

    # eseguiamo l'augmentation SOLO sul TRAIN SET
    training_data = AugmentedTrainingWrapper(training_base, data_dir)
    return training_data, val_data, test_data

# =====================================================================
# classe wrapper per il training che aggiunge i video derivanti dall'augmentation, MA SOLO SE siamo in fase di TRAIN
# altrimenti rischiamo di testare il modello su video che sono identici a quelli di train, ma semplicemente con le mani scambiate 
# =====================================================================
class AugmentedTrainingWrapper(Dataset):
    
    def __init__(self, base_train_subdataset, data_dir):
        self.base_train = base_train_subdataset
        self.data_dir = data_dir
        
        # Estrattore dei nomi dei file originali assegnati al train
        self.allowed_originals = set(base_train_subdataset.dataset.filenames[i] for i in base_train_subdataset.indices)
        
        # Cerchiamo tutti i file aumentati che derivano DA QUESTI specifici file di train
        self.augmented_filenames = []
        self.augmented_labels = []
        
        for filename in os.listdir(data_dir):
            if filename.endswith(".npy") and "_aug_" in filename:
                parts = filename.split("_aug_")
                original_name = parts[0] + ".npy"
                
                # Se l'originale è in questo training set, allora il suo clone è legale!
                if original_name in self.allowed_originals:
                    self.augmented_filenames.append(filename)
                    word = filename.split("_")[0]
                    self.augmented_labels.append(LABEL_MAP[word])

        print(f"   ↳ Trovati {len(self.augmented_filenames)} file aumentati legali per il Training Set.")

    def __len__(self):
        return len(self.base_train) + len(self.augmented_filenames)

    def __getitem__(self, idx):
        if idx < len(self.base_train):
            return self.base_train[idx]
        
        # Carichiamo i dati aumentati
        aug_idx = idx - len(self.base_train)
        filename = self.augmented_filenames[aug_idx]
        label = self.augmented_labels[aug_idx]
        
        data = np.load(self.data_dir / filename)
        real_len = data.shape[0]
        
        # Applichiamo il medesimo padding usando la variabile max_frames del dataset base
        padding = np.zeros((self.base_train.dataset.max_frames - real_len, data.shape[1]))
        data = np.vstack((data, padding))
        
        return torch.tensor(data, dtype=torch.float32), torch.tensor(label, dtype=torch.long), torch.tensor(real_len, dtype=torch.long)

# --- TEST DEL CAMERIERE ---
if __name__ == "__main__":
    print("Testo il PyTorch Dataset...")

    # Creiamo un'istanza del nostro Dataset
    my_dataset = SignLanguageDataset(PROCESSED_DIR)

    print(f"\nVideo totali trovati dal Dataset: {len(my_dataset)}")

    # Chiediamo al Dataset di darci il primo video in assoluto (indice 0)
    primo_video, prima_etichetta, prima_lunghezza = my_dataset[0]

    print("\nControllo Qualità sul primo video:")
    print(f"Formato del Tensore: {primo_video.shape}")
    print(f"Etichetta (Numero della parola): {prima_etichetta.item()}")
    print(f"Lunghezza Reale pre-padding: {prima_lunghezza.item()}")

    # Controllo dinamico sul test
    if primo_video.shape[0] == my_dataset.max_frames and primo_video.shape[1] == 402:
        print(
            f"\n-> GRANDIOSO! Il padding dinamico funziona. Il video è stato forzato a {my_dataset.max_frames} frame esatti."
        )
        print("Siamo ufficialmente pronti per scrivere la LSTM!")

