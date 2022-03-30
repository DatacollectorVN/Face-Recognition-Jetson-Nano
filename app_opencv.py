'''This is demo application using OpenCV, users can controll via terminal'''
import cv2
import os
import json
from src.photonic_face_recognition import PhotonicFaceRecognition
from src.utils import add_new_student_opencv, check_attendance_opencv, save_inference_config
import time

FILE_CONFIG = os.path.join("config", "inference.json")

def load_config(file_config):
    f = open(file_config)
    params = json.load(f)
    return params

def main(file_config):
    f = open(file_config)
    params = json.load(f)
    ans = True
    while ans:
        print("""
        1.Add new Student
        2.Check attendance
        3.Look up attendance
        4.Exit/Quit
        """)
        ans = input("What would you like to do? ")
        if ans == '1':
            params["UPDATE_DATABASES"] = True
            photonic_face_recognition = PhotonicFaceRecognition(**params)
            add_new_student_opencv(photonic_face_recognition, params)
        elif ans == '2':
            params["UPDATE_DATABASES"] = False
            photonic_face_recognition = PhotonicFaceRecognition(**params)
            check_attendance_opencv(photonic_face_recognition, params)
        elif ans == '3':
            print("\n Student Record Found")
        elif ans == '4':
            print("\n Goodbye")
            save_inference_config(params, file_config)
            ans = False
        else:
            print("\n Not Valid Choice Try again")
   

if __name__ == "__main__":
    main(file_config = FILE_CONFIG)