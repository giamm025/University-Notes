import os
import csv
import shutil
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import TARGET_WORDS, RAW_DIR, DATASETS_DIR

# prendiamo i percorsi specifici per il dataset ASL-Citizen
ASLCITIZEN_DIR = DATASETS_DIR / 'ASL_Citizen' / 'raw'
CSV_FILES = ['train.csv', 'val.csv', 'test.csv']
ASLCITIZEN_SPLIT_DIR  = ASLCITIZEN_DIR / 'ASL_Citizen' / 'splits'
ASLCITIZEN_VIDEOS_DIR = ASLCITIZEN_DIR / 'ASL_Citizen' / 'videos'


# funzione per estrarre da MSASL solo i video delle TARGET_WORDS e salvarli in data/raw/ con il formato "parola_dataset_id.mp4"
def parse_aslcitizen():

    print("Avvio parsing ASL-Citizen...")
    
    # trasformiamo il nostro formato formato (es. not-yet) nel formato ASL-Citizen (es. NOTYET)
    target_mapping = {}
    for w in TARGET_WORDS:
        clean_w = w.replace('-', '').upper() 
        target_mapping[clean_w] = w
        
    video_copiati = 0
    video_mancanti = 0
    word_counts = {word: 0 for word in TARGET_WORDS}
    
    # processiamo tutti e 3 i file CSV (Train, Val, Test)
    for csv_filename in CSV_FILES:

        csv_path = ASLCITIZEN_SPLIT_DIR / csv_filename
        if not csv_path.exists():
            print(f"File {csv_filename} non trovato in {ASLCITIZEN_SPLIT_DIR}. Lo salto.")
            continue
            
        print(f"\nLeggendo metadati da: {csv_filename}...")
        with csv_path.open(mode='r', encoding='utf-8') as f:
            
            reader = csv.DictReader(f)
            for row in reader:

                # prendiamo il gloss originale (es. NOTYET, UNDERSTAND1, etc.) e lo "normalizziamo"
                gloss = row['Gloss']
                base_gloss = gloss.rstrip('0123456789')
                
                # se la parola "pulita" fa parte delle nostre target_words
                if base_gloss in target_mapping:

                    # recuperiamo il nome originale
                    original_word = target_mapping[base_gloss] 
                    participant_id = row['Participant ID']
                    video_file = row['Video file']
                    source_path = ASLCITIZEN_VIDEOS_DIR / video_file
                    
                    # creiamo il nuovo filename (parola_dataset_id.mp4)
                    new_filename = f"{original_word}_aslcitizen_{participant_id}_{video_file}"
                    destination_path = RAW_DIR / new_filename
                    
                    # se abbiamo gia lavorato il video in passato (esiste già in data/raw/) => saltiamo 
                    if destination_path.exists():
                        word_counts[original_word] += 1
                        continue
                        
                    # controlliamo che il file video esista fisicamente
                    if source_path.exists():
                        shutil.copy(str(source_path), str(destination_path))
                        video_copiati += 1
                        word_counts[original_word] += 1
                        print(f"    ✅ Copiato: {new_filename} (Variante trovata: {gloss})")

                    else:
                        video_mancanti += 1
                        print(f"    ❌ Non trovato: {video_file} (Variante: {gloss})")

    print("\n--- RESOCONTO ASL-CITIZEN ---")
    for word, count in word_counts.items():
        print(f"Parola '{word}': {count} video validi")
        
    print(f"\nNuovi video copiati nell'imbuto: {video_copiati}")
    print(f"Video non trovati nella cartella originale: {video_mancanti}")


if __name__ == "__main__":
    parse_aslcitizen()