'''
Questo script apre tutti e tre i file JSON del MSASL Dataset (train, test, val) e cerca le nostre TARGET_WORDS 
(usando il campo "clean_text"). Per ogni parola trovata scarica il video temporaneamente, lo taglia (usando i 
campi "start_time" e "end_time") e infine lo salva in data/raw/.
'''

import json
import os
import sys
import yt_dlp
from pathlib import Path
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import TARGET_WORDS, RAW_DIR, DATASETS_DIR

# prendiamo i percorsi specifici per il dataset MSASL
MSASL_DIR = DATASETS_DIR / 'MS_ASL' / 'raw'
JSON_FILES = ['MSASL_train.json', 'MSASL_val.json', 'MSASL_test.json']
TEMP_DIR = DATASETS_DIR / 'MS_ASL' / 'temp' # Cartella per i video interi di YouTube

# controlliamo che esistano le cartelle necessarie, altrimenti le creiamo
TEMP_DIR.mkdir(parents=True, exist_ok=True)


# funzione per estrarre da MSASL solo i video delle TARGET_WORDS e salvarli in data/raw/ con il formato "parola_dataset_id.mp4"
def parse_msasl():

    video_creati = 0
    video_persi = 0
    word_counts = {word: 0 for word in TARGET_WORDS}
    
    # processiamo tutti e 3 i file JSON (Train, Val, Test)
    for json_filename in JSON_FILES:

        json_path = MSASL_DIR / json_filename
        if not json_path.exists():
            print(f"File {json_filename} non trovato, lo salto.")
            continue
            
        print(f"\nLettura dei metadati MSASL da: {json_filename}...")
        with json_path.open('r') as f:
            json_data = json.load(f)
            
        # per ogni entry (riga) del json
        for entry in json_data:

            # prendiamo la parola specifica nel campo "clean_text"
            word = entry.get('clean_text', '')
            if word in TARGET_WORDS:

                # prendiamo l'url del video
                url = entry.get('url')
                if not url.startswith('http'):
                    url = 'https://' + url
                    
                # prendiamo inizio e fine del video
                start_time = entry.get('start_time')
                end_time = entry.get('end_time')
                signer_id = entry.get('signer_id')
                
                # creiamo il nuovo filename (parola_dataset_id.mp4)
                new_filename = f"{word}_msasl_signer{signer_id}_{start_time}.mp4"
                final_path = RAW_DIR / new_filename
                temp_video_path = TEMP_DIR / f"temp_{signer_id}_{start_time}.mp4"
                
                # se abbiamo gia scaricato il video in passato (esiste già in data/raw/) => saltiamo 
                if final_path.exists():
                    print(f"⏭️ Salto: {new_filename} esiste già.")
                    word_counts[word] += 1
                    continue
                
                print(f"⏳ Processando [{word}] (da {start_time}s a {end_time}s)...")
                
                # scarichiamo il video intero da YouTube (lo salviamo temporaneamente in temp/)
                success = download_youtube_video(url, str(temp_video_path))
                
                # se il download ha successo => tagliamo il video
                if success:
                    try:
                        # TAGLIO RAPIDO (Senza ricompressione)
                        ffmpeg_extract_subclip(str(temp_video_path), start_time, end_time, targetname=str(final_path))
                        video_creati += 1
                        word_counts[word] += 1
                        print(f"    ✅ Salvato: {new_filename}")

                    except Exception as e:
                        print(f"    ❌ Errore nel taglio del video: {e}")

                    finally:
                        if temp_video_path.exists():
                            os.remove(str(temp_video_path))
                else:
                    video_persi += 1

    print("\n--- RESOCONTO MS-ASL ---")
    for word, count in word_counts.items():
        print(f"Parola '{word}': {count} video validi")
        
    print(f"\nNuovi video ritagliati e inseriti nell'imbuto: {video_creati}")
    print(f"Video non recuperabili (Link morti): {video_persi}")


# funzione per scricare i video (interi) da yt
def download_youtube_video(url, output_path):

    ydl_opts = {
        'format': 'bestvideo[height<=480][ext=mp4]',
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    
    except Exception as e:
        print(f"    ❌ Impossibile scaricare {url} (Forse rimosso da YouTube?)")
        return False
    

if __name__ == "__main__":
    parse_msasl()