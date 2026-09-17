import json
from pathlib import Path

''' 
==========================================================================
1. GESTIONE DEI PERCORSI (Pathlib)
==========================================================================
'''

ROOT_DIR        = Path(__file__).resolve().parent.parent
RAW_DIR         = ROOT_DIR / 'data'     / 'raw'
PROCESSED_DIR   = ROOT_DIR / 'data'     / 'processed'
LABELS_FILEPATH = ROOT_DIR / 'data'     / 'labels.json'
DATASETS_DIR    = ROOT_DIR / 'datasets'
MODELS_DIR      = ROOT_DIR / 'models'
RESULTS_DIR     = ROOT_DIR / 'results'

for directory in [RAW_DIR, PROCESSED_DIR, DATASETS_DIR, MODELS_DIR, RESULTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# le parole che utilizzeremo per costruire il nostro dataset, addestrare e testare il modello (prendendo solo i video relativi a queste parole)
TARGET_WORDS = ["happen", "finally", "late", "not-yet", "misunderstand", "understand"]

# aggiungiamo una classe "garbage" per tutte le parole che il modello "non riesce a riconoscere" (es. nessuna parola raggiunge una determinata threshold di confidenza)
GARBAGE_CLASS = "unknown"

SEED = 42

""" 
==========================================================================
GESTIONE VERSIONI
==========================================================================
L'idea è che ogni volta che implementiamo una nuova feature IMPORTANTE (es allarghiamo il dataset o tagliamo i keypoints del volto) 
documentiamo il tutto come fosse un nuovo modello proprio. una nuova versione. Se non facciamo cosi andremmo sempre a sovrascrivere 
il modello preccedente senz amantenere la "cronologia" dei miglioramenti. 
"""
EXPERIMENT_VERSION = "v3"
EXPERIMENT_DESC = "L_prova_webcam"
EXPERIMENT_SUFFIX = f"{EXPERIMENT_VERSION}_{EXPERIMENT_DESC}".strip('_')


"""Restituisce il path corretto per salvare/caricare il modello in base alla modalità."""
def GET_MODEL_PATH(modalita):
    return MODELS_DIR / f"model_{EXPERIMENT_SUFFIX}_{modalita}.pth"

"""Restituisce la cartella specifica dell'esperimento dentro results/ e la crea se non esiste."""
def GET_EXPERIMENT_DIR(modalita):
    exp_dir = RESULTS_DIR / EXPERIMENT_SUFFIX / modalita
    exp_dir.mkdir(parents=True, exist_ok=True)
    return exp_dir

"""Restituisce il path del file CSV per l'esperimento."""
def GET_CSV_PATH(modalita):
    csv_path = RESULTS_DIR / EXPERIMENT_SUFFIX / modalita / f"training_history.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    return csv_path

""" 
==========================================================================
GESTIONE ETICHETTE (LABELS)
==========================================================================
"""

# crea il labels.json basandosi sugli indici di TARGET_WORDS
def create_label_map():
    print(f"Creazione del dizionario immutabile in {LABELS_FILEPATH}...")
    label_map = {word: idx for idx, word in enumerate(TARGET_WORDS)}
    label_map[GARBAGE_CLASS] = len(TARGET_WORDS)
    with open(LABELS_FILEPATH, "w") as f:
        json.dump(label_map, f, indent=4)
    return label_map


# controlla: se labels.json lo carica, altrimenti lo crea (basandosi sugli indici di TARGET_WORDS)
def get_labels():

    # se il file NON esiste => lo crea (basandosi sugli indici di TARGET_WORDS)
    if not LABELS_FILEPATH.exists():
        return create_label_map()

    # altrimenti (gia esiste) => lo apre in sola lettura e lo carica in un dizionario
    with open(LABELS_FILEPATH, "r") as f:
        label_map = json.load(f)

        # check di consistenza: dobbiamo verificare che ci siano tutte le parole
        for word in TARGET_WORDS:
            if word not in label_map:
                print(f"ATTENZIONE: La parola '{word}' non è nel labels.json!")

        return label_map


LABEL_MAP = get_labels()
