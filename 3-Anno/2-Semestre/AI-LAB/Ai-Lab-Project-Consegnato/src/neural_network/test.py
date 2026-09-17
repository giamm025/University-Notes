import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import torch
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
from torch.utils.data import DataLoader
import argparse

from config import MODELS_DIR, RESULTS_DIR, PROCESSED_DIR, TARGET_WORDS, LABEL_MAP, SEED, EXPERIMENT_VERSION, EXPERIMENT_DESC, GARBAGE_CLASS
from neural_network.dataset import get_stratified_dataset_splits
from neural_network.model import SignLanguageLSTM

# =====================================================================
# FUNZIONI DI VISUALIZZAZIONE E REPORTING
# =====================================================================

"""Genera il grafico con le curve di Loss e Accuracy, per un confronto Train vs Val"""
def plot_learning_curves(csv_path, save_dir, modalita):

    if not csv_path.exists():
        print(f"⚠️ CSV non trovato in {csv_path}! Salto il grafico Learning Curve.")
        return
    # Prepariamo una "tela" bianca per il grafico grande 10x5 pollici
    plt.figure(figsize=(10, 5))

    # Legge il file CSV
    df = pd.read_csv(csv_path)

    # Disegniamo la prima linea: L'accuratezza durante lo studio (Train)
    plt.plot(df["Epoch"], df["Train_Acc"], label="Train Accuracy", marker="o")

    # Disegniamo la seconda linea: L'accuratezza durante l'esame (Val)
    plt.plot(df["Epoch"], df["Val_Acc"], label="Validation Accuracy", marker="s")

    # Aggiungiamo titoli, etichette per gli assi e una griglia di sfondo per renderlo "scientifico"
    plt.title(f"Learning Curves ({modalita})")
    plt.xlabel("Epochs (Epoche)")
    plt.ylabel("Accuracy (Accuratezza)")
    plt.ylim(0, 1.1)
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()

    # Salviamo l'immagine finita come .png nella cartella results/
    save_path = save_dir / f"learning_curve_{modalita}.png"
    plt.savefig(save_path)
    plt.close()
    print(f"📈 Grafico Learning Curve salvato in: {save_path}")


"""
Crea il report.txt che contiene:
    - Precision: quante volte il modello indovina la parola specifica?              (es. se dice "happen" 100 volte, quante volte ha ragione davvero?)
    - Recall:    se la parola X è presente 100 volte, quante volte la individua?
    - F1-Score:  è la media armonica tra Precision e Recall. RSe è alto, significa che va tutto bene: il modello è sia 
                 preciso che sensibile. Se è basso, significa che il modello ha problemi in almeno uno dei due aspetti.
    - Support:   quante volte la parola X è presente nel test set

I parametri della funzione sono:
    - solutions:    lista con i valori reali (quello che era davvero)
    - precitions:   lista con i valori predetti (quello che ha capito la rete)
    - target_words: lista con i nomi delle parole (ordinati in base agli indici di LABEL_MAP)
    - save_dir:     cartella dove salvare il report
    - modalita:     SOLO_MANI o MANI_VOLTO (per distinguere i file dei due esperimenti)
"""
def generate_report(solutions, precitions, target_words, save_dir, modalita):

    report = classification_report(solutions, precitions, labels=list(range(len(target_words))), target_names=target_words, zero_division=0)
    report_path = save_dir / f"classification_report_{modalita}.txt"

    with report_path.open("w", encoding="utf-8") as f:
        f.write(f"--- RISULTATI FINALI {modalita} ---\n\n")
        f.write(report)

    print(f"📝 Report Testuale salvato in: {report_path}")


"""
Crea la 'matrice di confusione', in cui:
    - confusion_matrix[x:y]: la risposta corretta era x ma il modello ha detto y

Da cui ne deduciamo che:
    - confusion_matrix[x:x]: quante volte il modello ha indovinato correttamente la parola x (la risposta corretta era x ma il modello ha detto x)
    - confusion_matrix[x:y]: quante volte il modello ha confuso la parola x con la parola y  (la risposta corretta era x ma il modello ha detto y)
"""
def draw_confusion_matrix(solutions, precitions, target_words, save_dir, modalita):
    cm = confusion_matrix(solutions, precitions)

    plt.figure(figsize=(10, 7)) 
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=target_words, yticklabels=target_words, cbar_kws={'label': 'Numero di video'})

    # aggiungiamo titoli ed etichette per rendere il grafico più chiaro e intuitivo
    plt.title(f"Confusion Matrix ({modalita})", fontsize=14, fontweight='bold', pad=15)
    plt.ylabel("Valore Reale (Quello che era davvero)", fontsize=12, fontweight='bold', labelpad=10)
    plt.xlabel("Valore Predetto (Quello che ha capito la rete)", fontsize=12, fontweight='bold', labelpad=10)
    
    # ruotiamo le etichette per renderle più leggibili, e aggiustiamo i margini
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    plt.tight_layout()

    cm_path = save_dir / f"confusion_matrix_{modalita}.png"
    plt.savefig(cm_path, dpi=150) 
    plt.close()
    print(f"📊 Confusion Matrix salvata in: {cm_path}")


"""
Carica il modello specificato e lo prepara per la fase di test. Garantisce RETROCOMPATIBILITÀ con i modelli 
v1_MANI_VOLTO (che aspettano 1530 coordinate piuttosto che 402 delle versioni successive)
"""
def load_trained_model(model_path, modalita, version, hidden_size, num_layers, device):
    # RETROCOMPATIBILITÀ: Se il modello è v1 ed è MANI_VOLTO, si aspetta 1530 ingressi, altrimenti 402
    if modalita == "SOLO_MANI":
        input_size = 126
    elif modalita == "MANI_VOLTO":
        input_size = 1530 if version == "v1" else 402
    else:
        raise ValueError("Modalità sconosciuta! Scegli SOLO_MANI o MANI_VOLTO.")
    num_classes = len(TARGET_WORDS)

    model = SignLanguageLSTM(input_size=input_size, hidden_size=hidden_size, num_classes=num_classes, num_layers=num_layers).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    return model


"""
Ri-esegue la fase di test per ottenere la lista di predizioni (risposte del modello) e la lista di soluzioni.
Include una logica di soglia di confidenza (Zero-Shot Thresholding): se il modello non è sicuro almeno al X% 
della sua risposta, la scarta e la classifica forzatamente come 'unknown'.

NB. Questa funzione qui è diversa da val_loop() di train.py!!!! Li eseguiamo il test AD OGNI EPOCA per ottenere LOSS e ACCURACY 
    di validation e decretare un "miglior modello" da salvare. 
    
    QUI, invece, eseguiamo il test solo sul MODELLO MIGLIORE per ottenere PREDICTIONS e SOLUTIONS, tramite cui potremo calcolare
    F1 Score, Confusion MAtrix, Report, Grafici etc... 
    
    Mischiare le due logice NON avrebbe senso poiche:
        - in tran.py ci ritroveremmo i dati per genrare grafici, che non servono a niente e rallentano l'esecuzione
        - in test.py ci ritroveremmo i dati per decretare il miglior modello, che non servono a niente siccome è gia 
                     stato scelto e salvato in precedenza da train.py
"""
def test_loop(model, dataloader, modalita, device, confidence_threshold=0.60):
    precitions = []
    solutions = []
    unknown_index = LABEL_MAP[GARBAGE_CLASS]
    print("🤖 Inizio test sul modello salvato...")
    with torch.no_grad():
        for x, y, lengths in dataloader:
            if modalita == "SOLO_MANI":
                x = x[:, :, :126]
            x, y, lengths = x.to(device), y.to(device), lengths.cpu()

            outputs = model(x, lengths)

            # --- LOGICA UNKNOWN CLASS (Soglia di Confidenza) ---
            # estraiamo la probabilità più alta e l'indice predetto
            probs = torch.softmax(outputs, dim=1)
            max_probs, preds = torch.max(probs, dim=1)
            low_confidence_mask = max_probs < confidence_threshold
            
            # forziamo le predizioni insicure a diventare 'unknown'
            preds[low_confidence_mask] = unknown_index

            # calcoliamo l'accuratezza
            precitions.extend(preds.cpu().numpy())
            solutions.extend(y.cpu().numpy())

    return solutions, precitions


# =====================================================================
# MAIN: ESECUZIONE DELLA VALUTAZIONE
# =====================================================================
if __name__ == "__main__":

    # ------------------------------------------ PARSER ------------------------------------------
    parser = argparse.ArgumentParser(description="Valuta il modello e genera grafici.")
    parser.add_argument("--modalita", type=str, choices=["SOLO_MANI", "MANI_VOLTO"], default="MANI_VOLTO")
    parser.add_argument("--version", type=str, help="Versione esperimento (es. v1, v2). Se omesso, usa config.py")
    parser.add_argument("--desc", type=str, help="Taglia dataset (es. S, M, L). Se omesso, usa config.py")
    parser.add_argument("--hidden_size", type=int, default=64)
    parser.add_argument("--num_layers", type=int, default=1)
    parser.add_argument("--threshold", type=float, default=0.60, help="Soglia di confidenza (es. 0.60 per 60%)")
    args = parser.parse_args()
    
    MODALITA = args.modalita
    VERSION  = args.version if args.version is not None else EXPERIMENT_VERSION
    DESC     = args.desc    if args.desc    is not None else EXPERIMENT_DESC
    
    # ------------------------------------------- PATHS ---------------------------------------
    suffix = f"{VERSION}_{DESC}".strip("_")
    SAVE_PATH = RESULTS_DIR / suffix / MODALITA
    SAVE_PATH.mkdir(parents=True, exist_ok=True)

    model_file = MODELS_DIR / f"model_{suffix}_{MODALITA}.pth"
    if not model_file.exists():
        print(f"❌ Errore: Modello non trovato ({model_file}). Salto valutazione.")
        sys.exit(1)
    csv_file = SAVE_PATH / "training_history.csv"

    if VERSION == "v3": dataset_folder_name = "v2_processed_L"
    else:               dataset_folder_name = f"{VERSION}_processed_{DESC}"
    dynamic_processed_dir = PROCESSED_DIR.parent / dataset_folder_name
    
    if not dynamic_processed_dir.exists():
        print(f"⚠️ Cartella specifica non trovata ({dynamic_processed_dir}). Uso PROCESSED_DIR di default.")
        dynamic_processed_dir = PROCESSED_DIR
    else:
        print(f"📦 Dataset rilevato con successo: {dataset_folder_name}")

    # ----------------------------------- FASE DI TEST E VALUTAZIONE ------------------------------------
    print(f"\n--- AVVIO VALUTAZIONE: {MODALITA} | Esperimento: {suffix} ---")
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # chiediamo a dataset.py di caricare i 3 diversi dataset (train, val, test), dopo aver effettauto lo split stratificato
    _, _, test_data = get_stratified_dataset_splits(dynamic_processed_dir, SEED)
    test_dataloader = DataLoader(test_data, batch_size=8, shuffle=False)

    # carichiamo il modello, eseguiamo la fase di test per ottenere soluzioni e predizioni, e poi generiamo i grafici e report finali
    model = load_trained_model(model_file, MODALITA, VERSION, args.hidden_size, args.num_layers, device)
    solutions, precitions = test_loop(model, test_dataloader, MODALITA, device, confidence_threshold=args.threshold)
    target_words = [word for word, idx in sorted(LABEL_MAP.items(), key=lambda item: item[1])]

    # ----------------------------------- GENERAZIONE GRAFICI E REPORT ------------------------------------
    plot_learning_curves(csv_file, SAVE_PATH, MODALITA)
    generate_report(solutions, precitions, target_words, SAVE_PATH, MODALITA)
    draw_confusion_matrix(solutions, precitions, target_words, SAVE_PATH, MODALITA)

    print(f"\n✅ Valutazione completata! Controlla la cartella: {SAVE_PATH}")