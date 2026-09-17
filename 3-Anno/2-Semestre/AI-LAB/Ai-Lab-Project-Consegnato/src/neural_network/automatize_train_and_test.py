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


# lista dei modelli da addestrare e testare
esperimenti = [
    {"version": "v1", "desc": "L", "modalita": "SOLO_MANI"},
    {"version": "v1", "desc": "L", "modalita": "MANI_VOLTO"},
    {"version": "v1", "desc": "M", "modalita": "SOLO_MANI"},
    {"version": "v1", "desc": "M", "modalita": "MANI_VOLTO"},
    {"version": "v1", "desc": "S", "modalita": "SOLO_MANI"},
    {"version": "v1", "desc": "S", "modalita": "MANI_VOLTO"},
    
    {"version": "v2", "desc": "L", "modalita": "MANI_VOLTO"},
    {"version": "v2", "desc": "M", "modalita": "MANI_VOLTO"},
    {"version": "v2", "desc": "S", "modalita": "MANI_VOLTO"},
]

# struttura per accumulare i dati per i grafici finali
plot_data = {
    ("v1", "SOLO_MANI"): {},
    ("v1", "MANI_VOLTO"): {},
    ("v2", "MANI_VOLTO"): {}
}

# =====================================================================
# FUNZIONI HELPER PER ESTRAZIONE METRICHE E STRUMENTAZIONE GRAFICI
# =====================================================================
"""Estrae Test Accuracy, Macro F1 e calcola l'Overfitting Gap."""
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
                if not parts:
                    continue
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
                is_old_format = 'Val_Acc' in rows[0]
                if is_old_format:
                    best_val_acc = -1.0
                    for row in rows:
                        try:
                            val_acc_curr = float(row['Val_Acc'])
                            if val_acc_curr > best_val_acc:
                                best_val_acc = val_acc_curr
                                train_acc = float(row['Train_Acc'])
                        except: pass
                else:
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



"""Genera un grafico a barre raggruppate per Test Acc, F1 e Gap, confrontando i diversi dataset S, M, L"""
def generate_comparison_chart(title, sizes_data, save_path):
    metrics_labels = ['Test Accuracy', 'F1-Score (Macro)', 'Overfitting Gap']
    
    s_vals = sizes_data.get('S', (0, 0, 0))
    m_vals = sizes_data.get('M', (0, 0, 0))
    l_vals = sizes_data.get('L', (0, 0, 0))

    s_bars = [s_vals[0], s_vals[1], s_vals[2]]
    m_bars = [m_vals[0], m_vals[1], m_vals[2]]
    l_bars = [l_vals[0], l_vals[1], l_vals[2]]

    x = np.arange(len(metrics_labels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(11, 6))
    
    rects1 = ax.bar(x - width, s_bars, width, label='Dataset Piccolo (S)', color='#1f77b4')
    rects2 = ax.bar(x, m_bars, width, label='Dataset Medio (M)', color='#2ca02c')
    rects3 = ax.bar(x + width, l_bars, width, label='Dataset Grande (L)', color='#d62728')

    ax.set_ylabel('Valore Metrica', fontsize=11, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics_labels, fontsize=12, fontweight='bold')
    
    all_values = s_bars + m_bars + l_bars
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


"""Genera tutti i grafici a barre richiamando la funzione generate_comparison_chart sopra"""
def generate_graphs():
    print("\n📊 Generazione dei grafici comparativi (Raggruppati per Metrica)...")
    for (v, mod), sizes_data in plot_data.items():
        if sizes_data:
            graph_title = f"Confronto Prestazioni Dataset - {v} ({mod})"
            graph_dir = RESULTS_DIR / "confronto_metriche"
            graph_dir.mkdir(parents=True, exist_ok=True)
            graph_filename = graph_dir / f"confronto_metriche_{v}_{mod}.png"
            
            generate_comparison_chart(graph_title, sizes_data, graph_filename)
            print(f"    ✅ Grafico salvato in: {graph_filename}")

# =====================================================================
# MAIN
# =====================================================================
if __name__ == "__main__":

    print("🚀 AVVIO PIPELINE COMPLETA: TRAINING & TEST\n")
    print("-" * 60)

    modelli_addestrati = 0
    modelli_valutati = 0
    errori = 0

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    for exp in esperimenti:

        # estraiamo i parametri dei singoli modelli da addestrare e valutare
        v = exp["version"]
        size = exp["desc"]
        mod = exp["modalita"]
        suffix = f"{v}_{size}".strip('_')
        nome_modello = f"model_{suffix}_{mod}"
        
        print(f"\n============================================================")
        print(f"🏋️  FASE 1: ADDESTRAMENTO -> {nome_modello}")
        print(f"============================================================")

        train_cmd = [sys.executable, str(TRAIN_SCRIPT), "--modalita", mod, "--version", v, "--desc", size]
        train_result = subprocess.run(train_cmd, capture_output=False, env=env)
        if train_result.returncode != 0:
            print(f"❌ Errore critico durante l'addestramento di {nome_modello}. Salto il Test.")
            errori += 1
            continue
        modelli_addestrati += 1
        
        print(f"\n------------------------------------------------------------")
        print(f"🔬 FASE 2: VALUTAZIONE -> {nome_modello}")
        print(f"------------------------------------------------------------")
        
        test_cmd = [sys.executable, str(TEST_SCRIPT), "--modalita", mod, "--version", v, "--desc", size]
        test_result = subprocess.run(test_cmd, capture_output=False, env=env)
        if test_result.returncode != 0:
            print(f"❌ Errore durante la valutazione di {nome_modello}.")
            errori += 1
            continue
        
        modelli_valutati += 1
        if (v, mod) in plot_data:
            save_dir = RESULTS_DIR / suffix / mod
            metrics = extract_metrics(save_dir, mod)
            plot_data[(v, mod)][size] = metrics

    generate_graphs()

    print("\n" + "=" * 60)
    print(f"🎉 PIPELINE COMPLETATA!")
    print(f"Modelli elaborati con successo: {modelli_addestrati} / {len(esperimenti)}")
    print(f"Modelli valutati con successo: {modelli_valutati} / {len(esperimenti)}")
    if errori > 0: print(f"Operazioni fallite: {errori}")
    print("=" * 60)

