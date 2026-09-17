import sys
from collections import Counter
from pathlib import Path

current_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(current_dir))

from config import PROCESSED_DIR, TARGET_WORDS

def count_npy_files():

    word_counts = {word: 0 for word in TARGET_WORDS}
    unknown_words = Counter()

    print(f"🔍 Scansionando la cartella: {PROCESSED_DIR}...\n")

    if not PROCESSED_DIR.exists():
        print("❌ La cartella 'processed' non esiste. Estrai prima le features!")
        return

    # Iteriamo su tutti i file .npy
    for npy_file in PROCESSED_DIR.glob("*.npy"):

        word = npy_file.name.split("_")[0]
        if word in word_counts:
            word_counts[word] += 1
        else:
            unknown_words[word] += 1

    print("=====================================================")
    print("📊 RESOCONTO FILE .NPY PER PAROLA")
    print("=====================================================")
    
    total_valid = 0
    for word in TARGET_WORDS:
        count = word_counts[word]
        total_valid += count
        warning = " ⚠️ NESSUN VIDEO!" if count == 0 else ""
        print(f"  - {word.ljust(15)}: {count} video{warning}")
        
    print("  ---------------------------------------------------")
    print(f"  🎯 TOTALE VIDEO VALIDI : {total_valid}")

    if unknown_words:
        print("\n⚠️ PAROLE EXTRA TROVATE (Non in TARGET_WORDS):")
        for word, count in unknown_words.items():
            print(f"  - {word}: {count} file")
            
    print("=====================================================")

if __name__ == "__main__":
    count_npy_files()