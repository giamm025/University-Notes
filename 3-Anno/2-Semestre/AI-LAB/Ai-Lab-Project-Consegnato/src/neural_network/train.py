import sys
import torch
from torch.utils.data import DataLoader, random_split
import torchmetrics
import argparse
import csv
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import TARGET_WORDS, PROCESSED_DIR, MODELS_DIR, RESULTS_DIR, SEED, EXPERIMENT_VERSION, EXPERIMENT_DESC, LABEL_MAP, GARBAGE_CLASS
from dataset import get_stratified_dataset_splits
from model import SignLanguageLSTM

# Forza stdout in UTF-8 nel caso in cui l'output venga reindirizzato su un file
if sys.stdout.encoding.lower() != "utf-8": sys.stdout.reconfigure(encoding="utf-8")

"""
0. ARGOMENTI DA TERMINALE
"""
parser = argparse.ArgumentParser(description="Addestra il modello di Riconoscimento LIS.")

arg_configs = [
    {"name": "--modalita", "type": str, "choices": ["SOLO_MANI", "MANI_VOLTO"], "default": "MANI_VOLTO"},
    {"name": "--version", "type": str, "help": "Versione esperimento (es. v1, v2). Se omesso, usa config.py"},
    {"name": "--desc", "type": str, "help": "Taglia dataset (es. S, M, L). Se omesso, usa config.py"},
    {"name": "--seed", "type": int, "default": 42},
    {"name": "--epochs", "type": int, "default": 200},
    {"name": "--batch_size", "type": int, "default": 8},
    {"name": "--patience", "type": int, "default": 10},
    {"name": "--learning_rate", "type": float, "default": 1e-3},
    {"name": "--hidden_size", "type": int, "default": 64},
    {"name": "--num_layers", "type": int, "default": 1},
    {"name": "--dropout", "type": float, "default": 0.0},
]

for arg in arg_configs:
    name = arg.pop("name")
    parser.add_argument(name, **arg)

args = parser.parse_args()
MODALITA = args.modalita
VERSION = args.version if args.version is not None else EXPERIMENT_VERSION
DESC = args.desc if args.desc is not None else EXPERIMENT_DESC
SEED = args.seed
EPOCHS = args.epochs
BATCH_SIZE = args.batch_size
PATIENCE = args.patience
LEARNING_RATE = args.learning_rate
HIDDEN_SIZE = args.hidden_size
NUM_LAYERS = args.num_layers
DROPOUT = args.dropout

# Costruzione path dinamici
suffix = f"{VERSION}_{DESC}".strip('_')
model_save_path = MODELS_DIR / f"model_{suffix}_{MODALITA}.pth"
experiment_save_dir = RESULTS_DIR / suffix / MODALITA
csv_path = experiment_save_dir / "training_history.csv"

# Assicuriamoci che la cartella dei risultati esista
experiment_save_dir.mkdir(parents=True, exist_ok=True)

torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)

print(f"\n⚙️  CONFIGURAZIONE AVVIATA: Modalità {MODALITA} | Esperimento {suffix} | Seed {SEED}")

"""
1. PREPARARE IL DATASET (Dinamico e Stratificato)
"""
# estraiamo il dataset giusto in base a versione e desc del modello che stiamo addestrando
if VERSION == "v3": dataset_folder_name = "v2_processed_L"
else:               dataset_folder_name = f"{VERSION}_processed_{DESC}"
dynamic_processed_dir = PROCESSED_DIR.parent / dataset_folder_name

if not dynamic_processed_dir.exists():
    print(f"⚠️ Cartella specifica non trovata ({dynamic_processed_dir}). Uso PROCESSED_DIR di default.")
    dynamic_processed_dir = PROCESSED_DIR
else:
    print(f"📦 Dataset rilevato con successo: {dataset_folder_name}")

# chiediamo a dataset.py di caricare i 3 diversi dataset (train, val, test), dopo aver effettauto lo split stratificato 
training_data, val_data, test_data = get_stratified_dataset_splits(dynamic_processed_dir, SEED)

print(f"Split dataset stratificato: {len(training_data)} train | {len(val_data)} val | {len(test_data)} test")

"""
2. CREARE I DATALOADER
"""
train_dataloader = DataLoader(training_data, batch_size=BATCH_SIZE, shuffle=True)
val_dataloader = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=False)
test_dataloader = DataLoader(test_data, batch_size=BATCH_SIZE, shuffle=False)

"""
3. SELEZIONARE IL DISPOSITIVO
"""
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
print(f"Using {device} device")

"""
3.5 CONFIGURAZIONE A/B TEST
"""
if MODALITA == "SOLO_MANI": input_size = 126
elif VERSION == "v1":       input_size = 1530  
else:                       input_size = 402

"""
4. DEFINIZIONE DEL MODELLO
"""
num_classes = len(TARGET_WORDS)

model = SignLanguageLSTM(
    input_size=input_size,
    hidden_size=HIDDEN_SIZE,
    num_classes=num_classes,
    num_layers=NUM_LAYERS,
    dropout=DROPOUT,
).to(device)

"""
5. IPERPARAMETRI E OPTIMIZER
"""
loss_fn = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
metric = torchmetrics.Accuracy(task="multiclass", num_classes=num_classes).to(device)

"""
6. TRAINING LOOP
"""
def train_loop(train_dataloader, model, loss_fn, optimizer):
    model.train()
    total_loss = 0

    for batch, (x, y, lengths) in enumerate(train_dataloader):
        if MODALITA == "SOLO_MANI":
            x = x[:, :, :126]

        x, y = x.to(device), y.to(device)

        pred = model(x, lengths)
        loss = loss_fn(pred, y)

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        total_loss += loss.item()
        metric(pred, y)

    epoch_acc = metric.compute().item()
    epoch_loss = total_loss / len(train_dataloader)

    print(f"---> Train Loss: {epoch_loss:.4f} | Train Acc: {epoch_acc:.4f}")
    metric.reset()
    return epoch_loss, epoch_acc

"""
7. VALIDATION LOOP
"""
def val_loop(dataloader, model, loss_fn, is_test=False, confidence_threshold=0.60):
    
    model.eval()
    total_loss = 0.0
    num_batches = 0
    
    # recuperiamo l'indice della classe "unknown"
    unknown_index = LABEL_MAP[GARBAGE_CLASS]

    with torch.no_grad():
        for x, y, lengths in dataloader:
            
            # se siamo in modalita SOLO_MANI tagliamo il tensore per escludere le coordinate del volto
            if MODALITA == "SOLO_MANI":
                x = x[:, :, :126]

            x, y = x.to(device), y.to(device)

            # prendiamo le risposte del modello e calcoliamo la loss, accumulando i risultati per poi fare la media alla fine dell'epoca
            pred = model(x, lengths)
            total_loss += loss_fn(pred, y).item()
            
            # --- LOGICA UNKNOWN CLASS (Soglia di Confidenza) ---
            # estraiamo la probabilità più alta e l'indice predetto
            probs = torch.softmax(pred, dim=1)
            max_probs, preds = torch.max(probs, dim=1)
            low_confidence_mask = max_probs < confidence_threshold
            
            # forziamo le predizioni insicure a diventare 'unknown'
            preds[low_confidence_mask] = unknown_index

            # calcoliamo l'accuratezza
            num_batches += 1
            metric(preds, y)

    avg_loss = total_loss / num_batches
    acc = metric.compute().item()
    
    prefix = "TEST" if is_test else "VAL "
    print(f"--- {prefix}  → Loss: {avg_loss:.4f} | Acc: {acc:.4f}")
    metric.reset()
    return avg_loss, acc

"""
8. ESECUZIONE E SALVATAGGIO
"""
print(f"Inizio addestramento in modalità: {MODALITA}")

history = []
patience = PATIENCE
epochs_no_improve = 0
best_val_loss = float("inf")

for epoch in range(EPOCHS):
    print(f"=============================")
    print(f" EPOCH: {epoch + 1}/{EPOCHS}")
    print(f"=============================")

    train_loss, train_acc = train_loop(train_dataloader, model, loss_fn, optimizer)
    val_loss, val_acc = val_loop(val_dataloader, model, loss_fn)

    history.append([epoch + 1, train_loss, train_acc, val_loss, val_acc])

    if val_loss < best_val_loss:
        best_val_loss = val_loss
        epochs_no_improve = 0
        torch.save(model.state_dict(), model_save_path)
        print(f"💾 Modello salvato! Nuova migliore Val Loss: {best_val_loss:.4f} (Val Acc: {val_acc:.4f})\n")
    else:
        epochs_no_improve += 1
        print(f"⚠️  Nessun miglioramento per {epochs_no_improve}/{patience} epoche consecutive.\n")

        if epochs_no_improve >= patience:
            print("🛑 EARLY STOPPING ATTIVATO: il modello ha smesso di imparare.")
            print(f"   Miglior Val Loss salvata: {best_val_loss:.4f}")
            break

with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Epoch", "Train_Loss", "Train_Acc", "Val_Loss", "Val_Acc"])
    writer.writerows(history)

print("\n" + "=" * 50)
print(f"\n✅ Addestramento completato! Modello salvato in: {model_save_path}")
print("🔬 VALUTAZIONE FINALE SUL TEST SET (solo per il miglior modello)")
print("=" * 50)
model.load_state_dict(torch.load(model_save_path, map_location=device, weights_only=True))
final_test_loss, final_test_acc = val_loop(test_dataloader, model, loss_fn, is_test=True)
print(f"*** ACCURATEZZA DI TEST FINALE: {final_test_acc:.4f} | Loss: {final_test_loss:.4f} ***")
print("=" * 50)
print("👉 Usa test.py (o bulk_evaluate.py) per valutare le performance sul Test Set e generare i grafici.")

print("\nAddestramento completato! 🎉")