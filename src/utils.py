import numpy as np
import json
import os
import cv2

### UTILITIES FUNCTION FOR `src/photonic_face_recognition`.
def update_config(params, known_face_names):
    params["CLASSES"] = known_face_names

def save_inference_config(params):
    JSON_FILE_DIR = os.path.join("config", "inference.json")
    with open(JSON_FILE_DIR, 'w') as file:
        json.dump(params, file)

def save_face_embed_vector(txt_file_dir, known_face_encodings, known_face_names):
    for i in range(len(known_face_encodings)):
        know_face_encoding = known_face_encodings[i]
        known_face_name = known_face_names[i]
        known_face_name = known_face_name.replace(' ', '_')
        np.savetxt(os.path.join(txt_file_dir, known_face_name + ".txt"), know_face_encoding, delimiter = ',')

### UTILITIES FUNCTION FOR `app_opencv.py`
def draw_fps(frame, fps):
    frame = cv2.putText(frame, f"FPS: {fps}", (0, 30), cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 255), 1)

    return frame

def user_controller_cmd():
    pass
