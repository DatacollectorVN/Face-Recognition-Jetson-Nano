'''This is demo application using OpenCV, users can controll via terminal'''
import cv2
import os
import json
from src.photonic_face_recognition import PhotonicFaceRecognition
from src.utils import draw_fps
import time
import numpy as np 
import sys

FILE_CONFIG = os.path.join("config", "inference.json")

def main(file_config):
    f = open(file_config)
    params = json.load(f)
    photonic_face_recognition = PhotonicFaceRecognition(**params)

    # Load avaiable instances in dataset.
    known_face_names = params["CLASSES"]
    known_face_encodings = photonic_face_recognition.load_know_face_encodings(params["TXT_FILE_DIR"], known_face_names)

    # setup 
    prev_frame_time = 0
    new_frame_time = 0
    video_capture = cv2.VideoCapture(0)
    process_this_frame = True
    while True:
        # Grab a single frame of video
        _, frame = video_capture.read()

        # down scale frame
        small_frame = photonic_face_recognition.down_scale_image(frame, params["DOWN_SCALE"])

        # convert frame to RGB
        rgb_small_frame = small_frame[:, :, ::-1]

        # Apply trick to increase FPS
        if process_this_frame:
            face_encodings, face_locations = photonic_face_recognition.face_encoding_algorithm(rgb_small_frame)
            face_names = photonic_face_recognition.face_recognition_algorithm(face_encodings, known_face_encodings, 
                                                                              known_face_names, params["TOLERANCE"])
        
        process_this_frame = not process_this_frame

        frame = photonic_face_recognition.face_recognition_drawning(frame, face_locations, face_names, params["DOWN_SCALE"])

        # calculate FPS
        new_frame_time = time.time()
        fps = int(1 / (new_frame_time - prev_frame_time))
        frame = draw_fps(frame, fps)
        prev_frame_time = new_frame_time
        
        # Display the resulting image
        cv2.imshow('Video', frame)

        # close all if press ESC
        key =  cv2.waitKey(1)
        if key == 27:
            break

if __name__ == "__main__":
    main(file_config = FILE_CONFIG)