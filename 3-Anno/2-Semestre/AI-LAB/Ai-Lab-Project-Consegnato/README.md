# Sign Language Recognition (LSTM + MediaPipe)

Progetto universitario di Machine Learning per il riconoscimento automatico della Lingua dei Segni Americana (ASL) tramite l'estrazione di keypoint spaziali con MediaPipe e la classificazione temporale con reti LSTM in PyTorch.


## 📂 Struttura delle Cartelle

```text
Ai-Lab-Project/
├── data/                       # Dati generati a runtime (non versionati)
│   ├── raw/                    # Clip video originali ritagliati (.mp4)
│   └── processed/              # Coordinate estratte via MediaPipe (.npy)
├── datasets/                   # Dati raw scaricati da Kaggle
├── models/                     # Checkpoint dei modelli PyTorch addestrati (.pth)
├── results/                    # Output (grafici, learning curve, matrici di confusione)
└── src/                        # Codice sorgente della pipeline
    ├── config.py               # Parametri globali, path e target words
    ├── extract_features.py     # Script principale estrazione feature
    ├── enlarge_dataset/        # Moduli per Download e Augmentation
    ├── parsers/                # Script di parsing specifici per dataset
    ├── neural_network/         # Dataset wrapper, architettura LSTM, loop di Train/Test
    └── webcam/                 # Script per l'inferenza su file e via webcam live
```

## ⚙️ Installazione

Assicurati di avere **Python 3.9 o superiore** installato sul tuo sistema.

**1. Clona la repository:**
```bash
git clone https://github.com/tuo-utente/Ai-Lab-Project.git
cd Ai-Lab-Project
```

**2. Crea e attiva un ambiente virtuale:**
```bash
# macOS/Linux
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

**3. Installa le dipendenze:**
```bash
pip install torch torchvision torchaudio torchmetrics mediapipe opencv-python numpy pandas matplotlib seaborn scikit-learn kagglehub yt-dlp moviepy
```
*(Nota: Se hai una GPU NVIDIA, assicurati di installare la versione di PyTorch compatibile con CUDA per accelerare il training).*

## 🚀 Utilizzo

La pipeline è progettata per essere eseguita in fasi sequenziali. Prima di iniziare, puoi configurare le parole da riconoscere (`TARGET_WORDS`) modificando il file `src/config.py`.

### Fase 1: Download e Parsing dei Dataset
Scarica i dataset grezzi ed estrai i clip video `.mp4` associati alle tue parole target.
```bash
python src/enlarge_dataset/download_datasets.py --dataset all
python src/parsers/MSASL_parser.py
python src/parsers/WLASL_parser.py
python src/parsers/ASLCitizen_parser.py
```

### Fase 2: Estrazione delle Feature
Converti i video `.mp4` in sequenze vettoriali (tensori NumPy `.npy`) tramite MediaPipe.
```bash
python src/extract_features.py
```

### Fase 3: Data Augmentation
Bilancia il numero di campioni per ogni classe generando variazioni sintetiche (il setup di base garantisce robustezza contro l'overfitting).
```bash
python src/enlarge_dataset/augment_dataset.py
```

### Fase 4: Addestramento del Modello (Training)
Avvia l'addestramento della rete LSTM. Puoi scegliere tra la modalità `MANI_VOLTO` o `SOLO_MANI`.
```bash
python src/neural_network/train.py --modalita MANI_VOLTO --epochs 200 --batch_size 8
```

### Fase 5: Valutazione (Test)
Verifica le performance del modello migliore salvato. Questo script genererà curve di apprendimento, matrici di confusione e classification report (in formato testuale e grafico) dentro la cartella `results/`.
```bash
python src/neural_network/test.py --modalita MANI_VOLTO
```

### Fase 6: Inferenza Live (Webcam)
Avvia l'applicativo per testare il modello in tempo reale! 
- Premi **R** per avviare/stoppare la registrazione di un gesto.
- Premi **Q** per uscire.
```bash
python src/webcam/webcam_inference.py --modalita MANI_VOLTO
```
