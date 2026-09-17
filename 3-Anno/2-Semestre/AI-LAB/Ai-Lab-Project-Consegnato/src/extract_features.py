import cv2
import mediapipe as mp
import numpy as np
from config import PROCESSED_DIR, RAW_DIR, LABEL_MAP

# ------------------------------------------------------------- MEDIA PIPE -------------------------------------------------------------
mp_holistic = mp.solutions.holistic


# funzione per processare un intero video: apre il video, lo divide in frame ed estrae i keypoints per ogni frame
# alla fine salva il risultato in un file NumPy pronto per essere utilizzato del modello LSTM
def process_video(video_path, save_path):

    # apriamo il video con OpenCV
    cap = cv2.VideoCapture(video_path)

    # prepariamo una lista vuota dove salvare le coordinate di ogni frame. ogni elemento di questa lista sarà un array
    # di 402 elementi: 63 per MANO SX + 63 per MANO DX + 276 per VOLTO FILTRATO (solo labbra, occhi, sopracciglia)
    frames_keypoints = []

    # avviamo il modello Holistic di MediaPipe (il un modello pre-addestrato per riconoscere le coordinate di mani, volto e corpo)
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

        # finche il video è aperto
        while cap.isOpened():

            # leggiamo un frame alla volta (ret è un bool che ci dice se il frame è stato letto correttamente;
            # frame è l'immagine vera e propria). se ret è False, significa che il video è finito o c'è stato
            # un errore nella lettura del frame... in entrambi i casi, usciamo dal ciclo
            ret, frame = cap.read()
            if not ret:
                break

            # solita conversione (openCV) BGR -> RGB (MediaPipe)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # estriamo i keypoints da MediaPipe
            mp_keypoints = holistic.process(frame_rgb)

            # estraiamo l'array e lo salviamo nella lista
            keypoints = convert_keypoints(mp_keypoints)
            frames_keypoints.append(keypoints)

        # una volta finito, rilasciamo il video per liberare le risorse
        cap.release()

    # trasformiamo la lista in un Array NumPy e lo salviamo in un file .npy pronto per essere utilizzato dal modello LSTM
    numpy_data = np.array(frames_keypoints)
    np.save(save_path, numpy_data)


# ---------------------------------------------------------------------------
# INDICI MEDIAPIPE
# ---------------------------------------------------------------------------
# LABBRA — 40 punti
NMM_LIPS = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95, 185, 40, 39, 37, 0, 267, 269, 270, 409, 415, 310, 311, 312, 13, 82, 81, 80, 191, 78]  # 40 landmark

# OCCHIO SINISTRO — 16 punti
NMM_LEFT_EYE = [249, 263, 362, 373, 374, 380, 381, 382, 384, 385, 386, 387, 388, 390, 398, 466]  # 16 landmark

# OCCHIO DESTRO — 16 punti 
NMM_RIGHT_EYE = [7, 33, 133, 144, 145, 153, 154, 155, 157, 158, 159, 160, 161, 163, 173, 246]  # 16 landmark

# SOPRACCIGLIO SINISTRO — 10 punti
NMM_LEFT_EYEBROW = [276, 282, 283, 285, 293, 295, 296, 300, 334, 336]  # 10 landmark

# SOPRACCIGLIO DESTRO — 10 punti
NMM_RIGHT_EYEBROW = [46, 52, 53, 55, 63, 65, 66, 70, 105, 107]  # 10 landmark

# Indice unico, ordinato, senza duplicati, usato per il filtraggio
NMM_FACE_INDICES = sorted(set(NMM_LIPS + NMM_LEFT_EYE + NMM_RIGHT_EYE + NMM_LEFT_EYEBROW + NMM_RIGHT_EYEBROW))


# funzione per convertire i risultati di MediaPipe in un array di 402 numeri
# (63 MANO SX + 63 MANO DX + 276 VOLTO FILTRATO)
def convert_keypoints(mp_keypoints):

    # estraiamo i keypoints per ogni parte del corpo
    left_hand = mp_keypoints.left_hand_landmarks
    right_hand = mp_keypoints.right_hand_landmarks
    face = mp_keypoints.face_landmarks

    # formiamo la lista di coordinare per la MANO SINISTRA
    temp_list = []
    if left_hand:
        for res in left_hand.landmark:
            temp_list.append([res.x, res.y, res.z])
        lh = np.array(temp_list).flatten()
    else:
        lh = np.zeros(21 * 3)

    # formiamo la lista di coordinare per la MANO DESTRA
    temp_list = []
    if right_hand:
        for res in right_hand.landmark:
            temp_list.append([res.x, res.y, res.z])
        rh = np.array(temp_list).flatten()
    else:
        rh = np.zeros(21 * 3)

    # formiamo la lista di coordinate per il VOLTO FILTRATO (solo NMM rilevanti)
    # invece di scorrere tutti i 468 landmark, accediamo solo agli indici in NMM_FACE_INDICES
    if face:
        all_landmarks = face.landmark
        filtered = [[all_landmarks[i].x, all_landmarks[i].y, all_landmarks[i].z] for i in NMM_FACE_INDICES]
        face_arr = np.array(filtered).flatten()  # 92 * 3 = 276 valori
    else:
        face_arr = np.zeros(len(NMM_FACE_INDICES) * 3) 

    return np.concatenate([lh, rh, face_arr])


# ------------------------------------------------------ 
# MAIN 
# ------------------------------------------------------
if __name__ == "__main__":

    print("\n--- INIZIO ESTRAZIONE MASSIVA (DA TUTTI I DATASET) ---")
    video_processati = 0
    video_saltati = 0

    # leggiamo TUTTI i file mp4 presenti nella cartella data/raw/ (indipendentemente da quale dataset provengano)
    for video_path in RAW_DIR.glob("*.mp4"):

        # dal filename estriamo la parola (il formato del nostro dataet è sempre parola_dataset_id.mp4)
        video_filename = video_path.name
        word = video_filename.split("_")[0]

        # costruiamo il path in cui effettuare il salvataggio
        save_path = PROCESSED_DIR / video_path.with_suffix(".npy").name

        # se il video è gia stato processato in passato => next
        if save_path.exists():
            video_saltati += 1
        else:
            print(f"Elaborazione: [{word}] -> {video_filename}...")
            process_video(str(video_path), str(save_path))
            video_processati += 1

    print("\n--- RESOCONTO FINALE ESTRAZIONE ---")
    print(f"Video processati: {video_processati}")
    print(f"Video già esistenti (saltati): {video_saltati}")
    print(f"Totale tensori pronti per la Rete Neurale: {video_processati + video_saltati}")
