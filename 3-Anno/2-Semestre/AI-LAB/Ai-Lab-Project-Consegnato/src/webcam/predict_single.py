"""
The script:
    1. Opens the video with OpenCV and runs it through MediaPipe Holistic.
    2. Displays the video in real-time with MediaPipe keypoint overlays.
    3. Extracts keypoints per frame using convert_keypoints() from extract_features.py.
    4. Builds a (1, seq_len, input_size) PyTorch tensor.
    5. Loads the trained SignLanguageLSTM checkpoint via GET_MODEL_PATH(modalita).
    6. Prints the predicted word and the softmax confidence score.
"""

import sys
import argparse
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent     
sys.path.insert(0, str(SRC_DIR))

import cv2
import numpy as np
import torch
import torch.nn.functional as F
import mediapipe as mp

from config import LABEL_MAP, TARGET_WORDS, GET_MODEL_PATH
from extract_features import convert_keypoints
from neural_network.model import SignLanguageLSTM

INPUT_SIZE = {
    "MANI_VOLTO": 402,   
    "SOLO_MANI":  126,   
}


"""
Reads hidden_size and num_layers directly from the checkpoint weights so we never have to hardcode them or keep them in sync manually.
"""
def infer_hyperparams_from_checkpoint(state_dict: dict) -> tuple[int, int]:
    hidden_size = state_dict["lstm.weight_hh_l0"].shape[1]
    num_layers  = sum(1 for k in state_dict if k.startswith("lstm.weight_hh_l"))
    return hidden_size, num_layers


"""Loads the trained LSTM checkpoint for the given modalita."""
def load_model(modalita: str, device: torch.device) -> SignLanguageLSTM:
    model_path = GET_MODEL_PATH(modalita)

    if not model_path.exists():
        raise FileNotFoundError(
            f"Checkpoint not found at: {model_path}\n"
            "Make sure you have trained the model with this modalita first."
        )

    state_dict = torch.load(model_path, map_location=device)
    hidden_size, num_layers = infer_hyperparams_from_checkpoint(state_dict)

    print(f"[INFO] Checkpoint hyperparams → hidden_size={hidden_size}, num_layers={num_layers}")

    model = SignLanguageLSTM(
        input_size=INPUT_SIZE[modalita],
        hidden_size=hidden_size,
        num_classes=len(TARGET_WORDS),
        num_layers=num_layers,
    )

    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()

    print(f"[INFO] Model loaded from: {model_path}")
    return model


"""
Opens the video with OpenCV, runs MediaPipe Holistic on every frame, displays the tracking visually, and returns a 
(seq_len, input_size) NumPy array of keypoints
"""
def extract_keypoints_from_video(video_path: str, modalita: str) -> np.ndarray:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file: {video_path}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps          = cap.get(cv2.CAP_PROP_FPS)
    
    delay = int(1000 / fps) if fps > 0 else 30
    
    print(f"[INFO] Video: {Path(video_path).name} | {total_frames} frames @ {fps:.1f} fps")

    frames_keypoints = []

    with mp.solutions.holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as holistic:

        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_results = holistic.process(frame_rgb)
            
            # --- DRAWING MEDIAPIPE HUD ---

            # Left Hand
            mp.solutions.drawing_utils.draw_landmarks(
                frame, mp_results.left_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS,
                mp.solutions.drawing_utils.DrawingSpec(color=(121, 22, 76),  thickness=2, circle_radius=4),
                mp.solutions.drawing_utils.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2),
            )
            # Right Hand
            mp.solutions.drawing_utils.draw_landmarks(
                frame, mp_results.right_hand_landmarks, mp.solutions.holistic.HAND_CONNECTIONS,
                mp.solutions.drawing_utils.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                mp.solutions.drawing_utils.DrawingSpec(color=(245, 66,  230), thickness=2, circle_radius=2),
            )
            # Face
            mp.solutions.drawing_utils.draw_landmarks(
                frame, mp_results.face_landmarks, mp.solutions.holistic.FACEMESH_CONTOURS,
                mp.solutions.drawing_utils.DrawingSpec(color=(80, 110, 10),  thickness=1, circle_radius=1),
                mp.solutions.drawing_utils.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1),
            )
            
            # Overlay frame info
            cv2.putText(frame, f"Processing Frame: {frame_idx + 1}/{total_frames}", (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(frame, "Press 'Q' to skip playback", (20, 75), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

            cv2.imshow("ASL Video Analysis Tracker", frame)
            
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                print("\n[INFO] Playback skipped by user. Processing remaining frames silently...")
                cv2.destroyWindow("ASL Video Analysis Tracker")
                delay = 1 

            # --- EXTRACTING VALUES ---
            keypoints = convert_keypoints(mp_results)   # always 402 values

            if modalita == "SOLO_MANI":
                keypoints = keypoints[:126]

            frames_keypoints.append(keypoints)
            frame_idx += 1

    cap.release()
    cv2.destroyAllWindows()

    if not frames_keypoints:
        raise ValueError("No frames were extracted from the video.")

    seq = np.array(frames_keypoints, dtype=np.float32)   # (seq_len, input_size)
    print(f"[INFO] Extracted keypoints: shape = {seq.shape}")
    return seq


"""
Converts the (seq_len, input_size) NumPy array to a (1, seq_len, input_size)
PyTorch tensor, passes it through the model, and returns probabilities
"""
def run_inference(seq: np.ndarray, model: SignLanguageLSTM, device: torch.device):
    seq_len    = seq.shape[0]
    tensor     = torch.tensor(seq, dtype=torch.float32).unsqueeze(0).to(device) 
    lengths    = torch.tensor([seq_len], dtype=torch.long)                        

    with torch.no_grad():
        logits      = model(tensor, lengths)         
        probs       = F.softmax(logits, dim=1)       
        confidence, pred_idx = probs.max(dim=1)

    pred_idx   = pred_idx.item()
    confidence = confidence.item() * 100.0           

    idx_to_word = {v: k for k, v in LABEL_MAP.items()}
    predicted_word = idx_to_word.get(pred_idx, f"<unknown idx {pred_idx}>")

    all_probs = {
        idx_to_word.get(i, str(i)): round(probs[0, i].item() * 100.0, 2)
        for i in range(probs.shape[1])
    }

    return predicted_word, confidence, all_probs


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Run sign-language prediction on a single .mp4 video.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--video_path",
        type=str,
        required=True,
        help="Path to the .mp4 video file to classify.",
    )
    parser.add_argument(
        "--modalita",
        type=str,
        default="MANI_VOLTO",
        choices=["MANI_VOLTO", "SOLO_MANI"],
        help='Feature set: "MANI_VOLTO" (hands+face, 402 features) or "SOLO_MANI" (hands only, 126 features).',
    )
    args = parser.parse_args()

    video_path = args.video_path
    modalita   = args.modalita

    # --- Validate inputs ---
    if not Path(video_path).exists():
        print(f"[ERROR] Video file not found: {video_path}")
        sys.exit(1)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[INFO] Using device: {device}")
    print(f"[INFO] Modalita:     {modalita}")
    print("-" * 50)

    # --- Load model ---
    model = load_model(modalita, device)

    # --- Extract keypoints ---
    seq = extract_keypoints_from_video(video_path, modalita)

    # --- Run inference ---
    predicted_word, confidence, all_probs = run_inference(seq, model, device)

    # --- Print results ---
    print("\n" + "=" * 50)
    print("           PREDICTION RESULT")
    print("=" * 50)
    print(f"  Word       : {predicted_word.upper()}")
    print(f"  Confidence : {confidence:.2f}%")
    print("-" * 50)
    print("  Full probability distribution:")
    for word, prob in sorted(all_probs.items(), key=lambda x: x[1], reverse=True):
        bar    = "█" * int(prob / 5)   # simple ASCII bar (max 20 chars)
        marker = " <--" if word == predicted_word else ""
        print(f"    {word:<15} {prob:6.2f}%  {bar}{marker}")
    print("=" * 50)