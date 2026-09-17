import os
import subprocess
import sys
import csv
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Forza stdout in UTF-8 nel caso in cui l'output venga reindirizzato su un file
if sys.stdout.encoding.lower() != "utf-8": sys.stdout.reconfigure(encoding="utf-8")

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import ROOT_DIR, RESULTS_DIR

CURRENT_DIR  = Path(__file__).resolve().parent
TRAIN_SCRIPT = CURRENT_DIR / "train.py"
TEST_SCRIPT  = CURRENT_DIR / "test.py"
MODELS_DIR   = ROOT_DIR / "models"
sys.path.append(str(CURRENT_DIR))

# lista delle configurazioni da addestrare e testare
esperimenti_tuning = [
    {
        "version": "v3", "desc": "tuning_1", "modalita": "MANI_VOLTO",
        "hidden_size": 64, "num_layers": 1, "learning_rate": 1e-3, "batch_size": 8, "patience": 15, "dropout": 0.0,
        "label": "Tuning 1 (64x1, Leggero)"
    },
    {
        "version": "v3", "desc": "tuning_2", "modalita": "MANI_VOLTO",
        "hidden_size": 256, "num_layers": 2, "learning_rate": 5e-4, "batch_size": 8, "patience": 20, "dropout": 0.0,
        "label": "Tuning 2 (256x2, Pesante - Overfitting)"
    },
    {
        "version": "v3", "desc": "tuning_3", "modalita": "MANI_VOLTO",
        "hidden_size": 128, "num_layers": 2, "learning_rate": 1e-3, "batch_size": 8, "patience": 20, "dropout": 0.4,
        "label": "Tuning 3 (128x2, Ottimale + Dropout 0.4)"
    },
]

# struttura per accumulare i dati per i grafici finali
tuning_metrics = {}

# =====================================================================
# FUNZIONI HELPER PER ESTRAZIONE METRICHE E STRUMENTAZIONE GRAFICI
# =====================================================================
"""Estrae Test Accuracy, Macro F1 e calcola l'Overfitting Gap"""
def extract_metrics(save_path, modalita):
    test_acc = 0.0
    macro_f1 = 0.0
    train_acc = 0.0

    # ------------------------------ TEST ACCURACY e F1-Score ------------------------------
    # prima di tutto dobbiamo leggere il report per estrarre Test Accuracy e Macro F1-Score
    report_path = save_path / f"classification_report_{modalita}.txt"
    if report_path.exists():
        with open(report_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.split()
                if not parts: continue
                if "macro" in parts and "avg" in parts:
                    try: macro_f1 = float(parts[4])
                    except: pass
                if "accuracy" in parts:
                    try: test_acc = float(parts[1])
                    except: pass

    # ------------------------------ TRAIN ACCURACY ------------------------------
    # poi, dobbiamo leggere la training_history.csv per estrarre la Train Accuracy migliore
    csv_path = save_path / "training_history.csv"
    if csv_path.exists():
        with open(csv_path, 'r', encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
            if rows:
                best_loss = float('inf')
                for row in rows:
                    loss_key = 'Test_Loss' if 'Test_Loss' in row else 'Val_Loss'
                    if loss_key in row:
                        try:
                            loss_val = float(row[loss_key])
                            if loss_val < best_loss:
                                best_loss = loss_val
                                train_acc = float(row['Train_Acc'])
                        except: pass
    else:
        print(f"⚠️ Attenzione: Impossibile trovare il file CSV in {csv_path}")

    # ------------------------------ OVERFITTING GAP ------------------------------
    overfitting_gap = train_acc - test_acc

    return test_acc, macro_f1, overfitting_gap

"""Genera un grafico a barre raggruppate per Test Acc, F1 e Gap, confrontando i diversi iperparametri"""
def generate_tuning_chart(title, data_dict, save_path):
    metrics_labels = ['Test Accuracy', 'F1-Score (Macro)', 'Overfitting Gap']
    
    t1_vals = data_dict.get('tuning_1', (0, 0, 0))
    t2_vals = data_dict.get('tuning_2', (0, 0, 0))
    t3_vals = data_dict.get('tuning_3', (0, 0, 0))

    t1_bars = [t1_vals[0], t1_vals[1], t1_vals[2]]
    t2_bars = [t2_vals[0], t2_vals[1], t2_vals[2]]
    t3_bars = [t3_vals[0], t3_vals[1], t3_vals[2]]

    x = np.arange(len(metrics_labels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(11, 6))
    
    rects1 = ax.bar(x - width, t1_bars, width, label='Tuning 1 (128x1, Veloce)', color='#9467bd')
    rects2 = ax.bar(x, t2_bars, width, label='Tuning 2 (128x2, Profondo)', color='#ff7f0e')
    rects3 = ax.bar(x + width, t3_bars, width, label='Tuning 3 (256x2, Gigante)', color='#17becf')

    ax.set_ylabel('Valore Metrica', fontsize=11, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_labels, fontsize=12, fontweight='bold')
    
    all_values = t1_bars + t2_bars + t3_bars
    min_val = min(all_values) if all_values else 0
    max_val = max(all_values) if all_values else 1
    ax.set_ylim(min_val - 0.15 if min_val < 0 else -0.05, max_val + 0.15)
    
    ax.axhline(0, color='black', linewidth=0.8, linestyle='-')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(fontsize=11, loc='upper right')

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            va_direction = 'bottom' if height >= 0 else 'top'
            offset = 3 if height >= 0 else -12
            ax.annotate(f'{height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, offset),  
                        textcoords="offset points",
                        ha='center', va=va_direction, fontsize=9, fontweight='bold')

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    fig.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


"""Genera un grafico a barre raggruppate per Test Acc, F1 e Gap, confrontando i diversi iperparametri"""
def generate_graph():
    print("\n📊 Generazione del grafico comparativo del Tuning...")
    if tuning_metrics:
        graph_title = f"Hyperparameter Tuning - {mod} (Dataset L)"
        graph_dir = RESULTS_DIR / "tuning"
        graph_dir.mkdir(parents=True, exist_ok=True)
        graph_filename = graph_dir / f"confronto_tuning_{v}.png"
        
        generate_tuning_chart(graph_title, tuning_metrics, graph_filename)
        print(f"    ✅ Grafico salvato in: {graph_filename}")

# =====================================================================
# MAIN
# =====================================================================
if __name__ == "__main__":
    print("🚀 AVVIO HYPERPARAMETER TUNING\n")
    print("-" * 60)

    modelli_addestrati = 0
    errori = 0
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    for exp in esperimenti_tuning:
        
        # estraiamo i parametri dei singoli modelli da addestrare e valutare
        v = exp["version"]
        desc = exp["desc"]
        mod = exp["modalita"]
        suffix = f"{v}_{desc}".strip('_')
        nome_modello = f"model_{suffix}_{mod}"
        
        print(f"\n============================================================")
        print(f"🏋️  FASE 1: ADDESTRAMENTO -> {exp['label']}")
        print(f"============================================================")
        
        train_cmd = [
            sys.executable, str(TRAIN_SCRIPT), 
            "--modalita", mod, 
            "--version", v, 
            "--desc", desc,
            "--hidden_size", str(exp["hidden_size"]),
            "--num_layers", str(exp["num_layers"]),
            "--learning_rate", str(exp["learning_rate"]),
            "--batch_size", str(exp["batch_size"]),
            "--patience", str(exp["patience"])
        ]
        train_result = subprocess.run(train_cmd, capture_output=False, env=env)
        
        if train_result.returncode != 0:
            print(f"❌ Errore critico durante l'addestramento di {nome_modello}. Salto il Test.")
            errori += 1
            continue
            
        print(f"\n✅ Addestramento di {nome_modello} completato.")
        modelli_addestrati += 1
        
        print(f"\n------------------------------------------------------------")
        print(f"🔬 FASE 2: VALUTAZIONE -> {exp['label']}")
        print(f"------------------------------------------------------------")
        
        test_cmd = [
            sys.executable, str(TEST_SCRIPT), 
            "--modalita", mod, 
            "--version", v, 
            "--desc", desc,
            "--hidden_size", str(exp["hidden_size"]),
            "--num_layers", str(exp["num_layers"])
        ]
        test_result = subprocess.run(test_cmd, capture_output=False, env=env)
        
        if test_result.returncode == 0:
            print(f"✅ Valutazione di {nome_modello} completata.")
            save_dir = RESULTS_DIR / suffix / mod
            metrics = extract_metrics(save_dir, mod)
            tuning_metrics[desc] = metrics
        else:
            print(f"❌ Errore durante la valutazione di {nome_modello}.")
            errori += 1

    print("\n" + "=" * 60)
    print(f"🎉 HYPERPARAMETER TUNING COMPLETATO!")
    print(f"Modelli elaborati con successo: {modelli_addestrati} / {len(esperimenti_tuning)}")
    if errori > 0: print(f"Operazioni fallite: {errori}")
    print("=" * 60)

    generate_graph()