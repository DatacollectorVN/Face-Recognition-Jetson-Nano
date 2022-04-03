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


class App:
    def __init__(self, window, FILE_CONFIG):
        # Init window of Tkinter app
        self.window = window
        self.window.title("Face Recognition App")
        self.window.geometry("%dx%d" % (self.window.winfo_screenwidth() , self.window.winfo_screenheight()))
        
        # Load params
        self.params = load_config(FILE_CONFIG)

        # Init widget
        header = tk.Label(master=window, text="Face Recognition App")
        btn_add = tk.Button(master=window, text="Add user", width=25, relief=tk.RAISED, borderwidth=5, command=self.add_user)
        btn_check = tk.Button(master=window, text="Check attendance", width=25, relief=tk.RAISED, borderwidth=5, command=self.check_user)
        btn_amount = tk.Button(master=window, text="Check list", width=25,  relief=tk.RAISED, borderwidth=5)
        btn_exit = tk.Button(master=window, text="Exit", width=25,  relief=tk.RAISED, borderwidth=5)

        # Position of widget
        header.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.1, anchor='n')
        btn_add.place(relx=0.05, rely=0.25, relwidth=0.2, relheight=0.1, anchor='nw')
        btn_check.place(relx=0.05, rely=0.4, relwidth=0.2, relheight=0.1, anchor='nw')
        btn_amount.place(relx=0.05, rely=0.55, relwidth=0.2, relheight=0.1, anchor='nw')
        btn_exit.place(relx=0.05, rely=0.7, relwidth=0.2, relheight=0.1, anchor='nw')

    def add_user(self):
        self.add_user_window = tk.Toplevel(self.window)
        self.add_user_window.geometry("%dx%d" % (self.add_user_window.winfo_screenwidth() , self.add_user_window.winfo_screenheight()))
        self.params["UPDATE_DATABASES"] = True
        photonic_face_recognition = PhotonicFaceRecognition(**self.params)
        entry_input_name = tk.Entry(master=self.add_user_window, textvariable=tk.StringVar())
        label_input_name = tk.Label(master=self.add_user_window, text="Input name:")
        button_snapshot = tk.Button(master=self.add_user_window, text="Snapshot", padx=5, pady=5, relief=tk.RAISED, borderwidth=5, \
            command=lambda: FaceRecognitionTkinter(self.add_user_window, entry_input_name.get(), photonic_face_recognition, self.params, FILE_CONFIG).snapshot_clicked())
        
        
        btn_enter = tk.Button(master=self.add_user_window, text="Enter", padx=5, pady=5, relief=tk.RAISED, borderwidth=5, \
            command=lambda: FaceRecognitionTkinter(self.add_user_window, entry_input_name.get(), photonic_face_recognition, self.params, FILE_CONFIG).show_camera())
        btn_back_home = tk.Button(master=self.add_user_window, text="Back home", padx=5, pady=5, relief=tk.RAISED, borderwidth=5, command=lambda: self.add_user_window.destroy())
        
        entry_input_name.place(relx=0.6, rely=0.2, relwidth=0.3, anchor='n', relheight=0.1)
        label_input_name.place(relx=0.35, rely=0.2, relwidth=0.2, anchor='n', relheight=0.1)
        btn_enter.place(relx=0.9, rely=0.25, relwidth=0.1, anchor='e', relheight=0.1)
        btn_back_home.place(relx=0.9, rely=0.4, relwidth=0.1, anchor='e', relheight=0.1)
        button_snapshot.place(relx=0.9, rely=0.55, relwidth=0.1, anchor='e', relheight=0.1)
        

    def check_user(self):
        self.params["UPDATE_DATABASES"] = False
        photonic_face_recognition = PhotonicFaceRecognition(**self.params)
        face_recognition = FaceRecognitionTkinter(self.window, None, photonic_face_recognition, self.params, FILE_CONFIG)
        face_recognition.check_attendance()

if __name__ == '__main__':
    window = tk.Tk()
    app = App(window, FILE_CONFIG)
    window.mainloop()