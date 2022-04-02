import json
import os
import tkinter as tk

from src.photonic_face_recognition import PhotonicFaceRecognition
from src.utils import FaceRecognitionTkinter

FILE_CONFIG = os.path.join("config", "inference.json")

def load_config(file_config):
    f = open(file_config)
    params = json.load(f)
    return params

def add_user():
    params["UPDATE_DATABASES"] = True
    photonic_face_recognition = PhotonicFaceRecognition(**params)
    entry_input_name = tk.Entry(master=window, textvariable=tk.StringVar())
    label_input_name = tk.Label(master=window, text="Input name:")
    btn_enter = tk.Button(master=window, text="Enter", padx=5, pady=5, relief=tk.RAISED, borderwidth=5, \
        command=lambda: FaceRecognitionTkinter(window, entry_input_name.get(), photonic_face_recognition, params, FILE_CONFIG).show_camera())
    
    entry_input_name.place(relx=0.6, rely=0.2, relwidth=0.3, anchor='n', relheight=0.1)
    label_input_name.place(relx=0.35, rely=0.2, relwidth=0.2, anchor='n', relheight=0.1)
    btn_enter.place(relx=0.95, rely=0.25, relwidth=0.1, anchor='e', relheight=0.1)

def check_user():
    params["UPDATE_DATABASES"] = False
    photonic_face_recognition = PhotonicFaceRecognition(**params)
    face_recognition = FaceRecognitionTkinter(window, None, photonic_face_recognition, params, FILE_CONFIG)
    face_recognition.check_attendance()

# Init window of Tkinter app
window = tk.Tk()
window.title("Face Recognition App")
window.geometry("%dx%d" % (window.winfo_screenwidth() , window.winfo_screenheight()))

# Load params
params = load_config(FILE_CONFIG)

# Init widget
header = tk.Label(master=window, text="Face Recognition App")
btn_add = tk.Button(master=window, text="Add user", width=25, relief=tk.RAISED, borderwidth=5, command=add_user)
btn_check = tk.Button(master=window, text="Check attendance", width=25, relief=tk.RAISED, borderwidth=5, command=check_user)
btn_amount = tk.Button(master=window, text="Check list", width=25,  relief=tk.RAISED, borderwidth=5)
btn_exit = tk.Button(master=window, text="Exit", width=25,  relief=tk.RAISED, borderwidth=5)

# Position of widget
header.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.1, anchor='n')
btn_add.place(relx=0.05, rely=0.25, relwidth=0.2, relheight=0.1, anchor='nw')
btn_check.place(relx=0.05, rely=0.4, relwidth=0.2, relheight=0.1, anchor='nw')
btn_amount.place(relx=0.05, rely=0.55, relwidth=0.2, relheight=0.1, anchor='nw')
btn_exit.place(relx=0.05, rely=0.7, relwidth=0.2, relheight=0.1, anchor='nw')



window.mainloop()