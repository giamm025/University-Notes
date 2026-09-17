"""
Real-time sign-language inference from a webcam feed.
After inference the predicted word and confidence are displayed in
the top-right corner until the next recording starts.
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

from config import LABEL_MAP, TARGET_WORDS, MODELS_DIR, EXPERIMENT_VERSION, EXPERIMENT_DESC, GARBAGE_CLASS
from extract_features import convert_keypoints
from neural_network.model import SignLanguageLSTM


INPUT_SIZE = {
    "MANI_VOLTO": 402,   
    "SOLO_MANI":  126,
}

COLOR_RED    = (0,   0,   220)
COLOR_GREEN  = (0,   200, 80)
COLOR_WHITE  = (255, 255, 255)
COLOR_BLACK  = (0,   0,   0)
COLOR_YELLOW = (0,   220, 220)
COLOR_DARK   = (30,  30,  30)




"""
Reads hidden_size and num_layers directly from the checkpoint weights
so we never have to hardcode them or keep them in sync manually.
"""
def infer_hyperparams_from_checkpoint(state_dict: dict) -> tuple[int, int]:
    hidden_size = state_dict["lstm.weight_hh_l0"].shape[1]
    num_layers  = sum(1 for k in state_dict if k.startswith("lstm.weight_hh_l"))
    return hidden_size, num_layers


def load_model(modalita: str, version: str, desc: str, device: torch.device) -> SignLanguageLSTM:

    suffix = f"{version}_{desc}".strip('_')
    model_path = MODELS_DIR / f"model_{suffix}_{modalita}.pth"

    if not model_path.exists():
        raise FileNotFoundError(
            f"Checkpoint not found at: {model_path}\n"
            "Train the model first, then re-run this script."
        )

    state_dict = torch.load(model_path, map_location=device, weights_only=True)
    hidden_size, num_layers = infer_hyperparams_from_checkpoint(state_dict)

    print(f"[INFO] Checkpoint hyperparams → hidden_size={hidden_size}, num_layers={num_layers}")

    input_dim = 1530 if (modalita == "MANI_VOLTO" and version == "v1") else INPUT_SIZE[modalita]

    model = SignLanguageLSTM(
        input_size=input_dim,
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
Takes the raw list of per-frame keypoint arrays, converts to a tensor,
and returns (predicted_word, confidence_pct, all_probs_dict).
"""
def run_inference(frames_keypoints: list, modalita: str,
                  model: SignLanguageLSTM, device: torch.device,
                  confidence_threshold: float = 0.60):
    if not frames_keypoints:
        return None, 0.0, {}

    seq     = np.array(frames_keypoints, dtype=np.float32)  
    seq_len = seq.shape[0]
    tensor  = torch.tensor(seq).unsqueeze(0).to(device)     
    lengths = torch.tensor([seq_len], dtype=torch.long)

    with torch.no_grad():
        logits     = model(tensor, lengths)
        probs      = F.softmax(logits, dim=1)
        conf, pidx = probs.max(dim=1)

    pidx           = pidx.item()
    confidence_val = conf.item() 
    confidence_pct = confidence_val * 100.0
    
    idx_to_word = {v: k for k, v in LABEL_MAP.items()}
    
    if confidence_val < confidence_threshold:
        predicted = GARBAGE_CLASS
    else:
        predicted = idx_to_word.get(pidx, f"<unknown {pidx}>")

    all_probs   = {
        idx_to_word.get(i, str(i)): round(probs[0, i].item() * 100.0, 2)
        for i in range(probs.shape[1])
    }
    return predicted, confidence_pct, all_probs



"""Draws a semi-transparent filled rectangle on the frame (in-place)."""
def draw_filled_rect_alpha(frame, x1, y1, x2, y2, color, alpha=0.55):
    overlay = frame.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)


"""
Overlays all HUD elements on the frame:
    - Top bar with mode label
    - REC indicator (when recording)
    - Frame counter (when recording)
    - Prediction panel (after inference)
    - Bottom help bar
"""
def draw_hud(frame, is_recording: bool, frame_count: int,
             result: dict, modalita: str, version: str, desc: str):
    h, w = frame.shape[:2]


    draw_filled_rect_alpha(frame, 0, 0, w, 42, COLOR_DARK, alpha=0.70)
    cv2.putText(frame, f"ASL Inference  |  modalita: {modalita} | {version}_{desc}",
                (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.65, COLOR_WHITE, 1, cv2.LINE_AA)


    draw_filled_rect_alpha(frame, 0, h - 38, w, h, COLOR_DARK, alpha=0.70)
    cv2.putText(frame, "R: toggle recording   |   Q: quit",
                (10, h - 14), cv2.FONT_HERSHEY_SIMPLEX, 0.55, COLOR_WHITE, 1, cv2.LINE_AA)


    if is_recording:
        draw_filled_rect_alpha(frame, 8, 52, 220, 90, COLOR_DARK, alpha=0.60)
        cv2.circle(frame, (28, 71), 10, COLOR_RED, -1, cv2.LINE_AA)
        cv2.putText(frame, "REC", (44, 78),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, COLOR_RED, 2, cv2.LINE_AA)
        cv2.putText(frame, f"frames: {frame_count}",
                    (110, 78), cv2.FONT_HERSHEY_SIMPLEX, 0.55, COLOR_YELLOW, 1, cv2.LINE_AA)


    if result and result.get("word"):
        word  = result["word"].upper()
        conf  = result["confidence"]
        probs = result.get("all_probs", {})

        panel_x, panel_y = w - 260, 52
        panel_w, panel_h = 252, 30 + 22 * (len(probs) + 1) + 10

        draw_filled_rect_alpha(frame, panel_x, panel_y,
                               panel_x + panel_w, panel_y + panel_h,
                               COLOR_DARK, alpha=0.72)


        cv2.putText(frame, word,
                    (panel_x + 8, panel_y + 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, COLOR_GREEN, 2, cv2.LINE_AA)


        cv2.putText(frame, f"{conf:.1f}%",
                    (panel_x + 160, panel_y + 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_YELLOW, 1, cv2.LINE_AA)


        sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)
        for i, (w_label, pct) in enumerate(sorted_probs):
            row_y    = panel_y + 50 + i * 22
            bar_full = 160
            bar_w    = int(bar_full * pct / 100)
            bar_col  = COLOR_GREEN if w_label.upper() == word else (80, 80, 80)


            cv2.rectangle(frame,
                          (panel_x + 80, row_y - 12),
                          (panel_x + 80 + bar_full, row_y + 2),
                          (60, 60, 60), -1)

            if bar_w > 0:
                cv2.rectangle(frame,
                              (panel_x + 80, row_y - 12),
                              (panel_x + 80 + bar_w, row_y + 2),
                              bar_col, -1)

            cv2.putText(frame, f"{w_label:<11}",
                        (panel_x + 6, row_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.42, COLOR_WHITE, 1, cv2.LINE_AA)
            cv2.putText(frame, f"{pct:.1f}%",
                        (panel_x + 246, row_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.38, COLOR_WHITE, 1, cv2.LINE_AA)




def main():
    parser = argparse.ArgumentParser(
        description="Real-time ASL inference from webcam with R-key recording toggle.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--modalita", type=str, default="MANI_VOLTO", choices=["MANI_VOLTO", "SOLO_MANI"])
    parser.add_argument("--version", type=str, help="Versione esperimento (es. v1, v2). Se omesso, usa config.py")
    parser.add_argument("--desc", type=str, help="Taglia dataset (es. S, M, L). Se omesso, usa config.py")
    parser.add_argument("--threshold", type=float, default=0.60, help="Soglia di confidenza (es. 0.60 per 60%)")
    parser.add_argument("--camera_index", type=int, default=0)
    args = parser.parse_args()

    modalita     = args.modalita
    camera_index = args.camera_index
    
    version = args.version if args.version is not None else EXPERIMENT_VERSION
    desc =    args.desc    if args.desc    is not None else EXPERIMENT_DESC

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[INFO] Device:    {device}")
    print(f"[INFO] Modalita:  {modalita}")
    print(f"[INFO] Version:   {version}_{desc}")


    model = load_model(modalita, version, desc, device)


    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"[ERROR] Cannot open camera at index {camera_index}.")
        sys.exit(1)


    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print("\n[INFO] Webcam opened. Press R to start/stop recording, Q to quit.")
    print("       Window must be in focus for key events to register.\n")


    is_recording       = False
    frames_keypoints   = []   
    result             = {}   

    with mp.solutions.holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as holistic:

        while True:
            ret, frame = cap.read()
            if not ret:
                print("[WARNING] Frame read failed, retrying...")
                continue


            frame = cv2.flip(frame, 1)


            frame_rgb  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_rgb.flags.writeable = False
            mp_results = holistic.process(frame_rgb)
            frame_rgb.flags.writeable = True


            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                mp_results.left_hand_landmarks,
                mp.solutions.holistic.HAND_CONNECTIONS,
                mp.solutions.drawing_utils.DrawingSpec(color=(121, 22, 76),  thickness=2, circle_radius=4),
                mp.solutions.drawing_utils.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2),
            )
            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                mp_results.right_hand_landmarks,
                mp.solutions.holistic.HAND_CONNECTIONS,
                mp.solutions.drawing_utils.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                mp.solutions.drawing_utils.DrawingSpec(color=(245, 66,  230), thickness=2, circle_radius=2),
            )
            mp.solutions.drawing_utils.draw_landmarks(
                frame,
                mp_results.face_landmarks,
                mp.solutions.holistic.FACEMESH_CONTOURS,
                mp.solutions.drawing_utils.DrawingSpec(color=(80, 110, 10),  thickness=1, circle_radius=1),
                mp.solutions.drawing_utils.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1),
            )


            if is_recording:
                kp = convert_keypoints(mp_results)   
                if modalita == "SOLO_MANI":
                    kp = kp[:126]
                frames_keypoints.append(kp)


            draw_hud(
                frame,
                is_recording=is_recording,
                frame_count=len(frames_keypoints),
                result=result,
                modalita=modalita,
                version=version,
                desc=desc
            )

            cv2.imshow("ASL Webcam Inference", frame)


            key = cv2.waitKey(1) & 0xFF

            if key == ord("q") or key == ord("Q"):
                print("[INFO] Quit requested.")
                break

            elif key == ord("r") or key == ord("R"):
                if not is_recording:

                    is_recording     = True
                    frames_keypoints = []
                    result           = {}
                    print("[INFO] Recording STARTED — perform your sign now.")

                else:

                    is_recording = False
                    n_frames     = len(frames_keypoints)
                    print(f"[INFO] Recording STOPPED — {n_frames} frames collected.")

                    if n_frames < 5:
                        print("[WARNING] Too few frames for reliable inference. "
                              "Try recording a longer gesture.")
                        result = {"word": "TOO SHORT", "confidence": 0.0, "all_probs": {}}
                    else:
                        predicted, confidence, all_probs = run_inference(
                            frames_keypoints, modalita, model, device, args.threshold
                        )
                        result = {
                            "word":       predicted,
                            "confidence": confidence,
                            "all_probs":  all_probs,
                        }
                        print(f"[RESULT] Predicted: {predicted.upper()}  "
                              f"| Confidence: {confidence:.2f}%")

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Webcam released. Goodbye!")


if __name__ == "__main__":
    main()