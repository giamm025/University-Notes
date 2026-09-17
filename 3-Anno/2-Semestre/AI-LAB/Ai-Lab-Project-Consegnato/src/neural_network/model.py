import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

"""
Come abbiamo visto a lezione dovremo implementare due metodi principali:

    - __init__(self): definiamo l'hardware, cioe la struttura del modello, ovvero quali tipi di layer 
                      utilizzeremo e come sono connessi tra loro.

    - forward(self, x): definiamo il software, cioe il flusso dei dati attraverso il modello, come i dati 
                        vengono trasformati dai layer per produrre l'output.
"""


class SignLanguageLSTM(nn.Module):

    # parametri:
    # - input_size:  quanti numeri entrano per ogni frame?
    #                (126 se lavoriamo "Solo Mani", 402 per "Mani+Volto")
    # - hidden_size: quanto è grande la memoria interna (hidden emmory) della LSTM?
    #                (Es. 64 o 128 neuroni. Piu è grande, più la rete può ricordare, ma più è difficile da addestrare)
    # - num_classes: il numero di canali di uscita... cioe: quali sono le soluzioni possibili?
    #                (nel nostro caso è il numero di parole che vogliamo riconoscere, cioè 6)
    # # - dropout:   probabilità di dropout tra LSTM e fc layer (default 0.0 = disabilitato)
    def __init__(self, input_size, hidden_size, num_classes=1, num_layers=1, dropout=0.0):
        super().__init__()

        # "legge” un intero video, un frame alla volta, e salva nella sua memoria interna (hidden state) un’array di numero che,
        # matematicamente, rappresentano il movimento osservato da inizio video fino a quel frame.
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
        )
        # serve a specificare l'ordine dei numeri nel tensore di input.
        # se batch_first=True,  la LSTM si aspetta (batch_size, seq_len, input_size).
        # se batch_first=False, la LSTM si aspetta (seq_len, batch_size, input_size).
        # la LSTM restituirà l'intera lista di ciò che ha pensato ad ogni frame de video

        # Se dropout=0.0 (default), nn.Dropout(0.0) è un no-op: non fa nulla.
        # Valori tipici da provare: 0.3, 0.5
        self.dropout = nn.Dropout(p=dropout)

        # creiamo lo stato lineare finale, che prende in input l'ultimo frame prodotto dalla LSTM e restituitsce
        # l'array con le probabilità di ciascuna parola (es. [0.1, 0.7, 0.05, 0.1, 0.05] => 10% "hello", 70% "book", ecc.)
        self.fc = nn.Linear(hidden_size, num_classes)

    # questa è la funzione che viene chiamata quando passiamo i dati alla rete. Definisce il PERCORSO che fanno i dati (da x fino alla predizione).
    def forward(self, x, lengths):

        # impachettiamo la sequenza per dire alla LSTM dove finisce ogni video reale
        # in questo modo la LSTM non spreca tempo a processare i frame di padding (tutti zeri)
        packed = pack_padded_sequence(
            x,
            lengths.cpu(),  # pack_padded_sequence vuole i lengths sulla CPU, non sulla GPU
            batch_first=True,
            enforce_sorted=False,  # non è necessario che il batch sia ordinato per lunghezza
        )

        # passiamo la sequenza impacchettata alla LSTM
        # hn conterrà lo stato nascosto all'ULTIMO frame REALE di ogni video (non all'ultimo frame di padding)
        _, (hn, _) = self.lstm(packed)

        # hn ha forma [num_layers, batch_size, hidden_size]
        # prendiamo l'ultimo layer (-1) per ottenere la decisione finale
        out = hn[-1]  # forma: [batch_size, hidden_size]

        # Durante model.eval() il dropout viene automaticamente disabilitato da PyTorch.
        out = self.dropout(out)

        # passiamo al layer lineare per ottenere le probabilità di ogni parola
        result = self.fc(out)
        return result


# --- TEST DELL'ARCHITETTURA ---
if __name__ == "__main__":
    from config import TARGET_WORDS

    print("Testo l'architettura della Rete Neurale...\n")

    batch_size = 8
    seq_len = 108
    num_classes = len(TARGET_WORDS)
    hidden_size = 64

    # Test con dropout
    input_size_mani = 126
    fake_data = torch.randn(batch_size, seq_len, input_size_mani)
    fake_lengths = torch.full((batch_size,), seq_len, dtype=torch.long)

    # Test senza dropout (default)
    model_no_drop = SignLanguageLSTM(input_size=input_size_mani, hidden_size=hidden_size, num_classes=num_classes, dropout=0.0)
    out_no_drop = model_no_drop(fake_data, fake_lengths)
    print(f"[dropout=0.0] Output shape: {out_no_drop.shape} -> (Deve essere: [{batch_size}, {num_classes}])")

    # Test con dropout attivo
    model_with_drop = SignLanguageLSTM(input_size=input_size_mani, hidden_size=hidden_size, num_classes=num_classes, dropout=0.5)
    model_with_drop.train()
    out_with_drop = model_with_drop(fake_data, fake_lengths)
    print(f"[dropout=0.5] Output shape: {out_with_drop.shape} -> (Deve essere: [{batch_size}, {num_classes}])")

    if out_no_drop.shape == (batch_size, num_classes):
        print("\n-> ARCHITETTURA OK! Il dropout è stato aggiunto correttamente.")
