import json
import copy
import os
import tkinter as tk
from PIL import ImageTk, Image

from src.photonic_face_recognition import PhotonicFaceRecognition
from src.utils import save_inference_config, check_attendance_opencv, add_new_student_tkinter
from src.face_recognition_tkinter import FaceRecognitionTkinter
from src.virtual_keyboard import VirtualKeyboardJetson

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
        # self.window.attributes('-fullscreen', True)
        self.window.geometry("%dx%d+0+0" % (self.window.winfo_screenwidth() , self.window.winfo_screenheight()))

        # Load params
        self.file_config = FILE_CONFIG
        self.params = load_config(self.file_config)
        self.logo_bme = ImageTk.PhotoImage(Image.open(
            "public-imgs/logo_bme.png").resize((100, 100), Image.ANTIALIAS))

        # Init widget
        self.header = tk.Label(master=window, text="Face Recognition App", font=("Helvetica", 40))
        self.logo_bme_frame = tk.Frame(master=window)
        btn_add = tk.Button(master=window, text="Add user", width=25, font=("Helvetica", 20),
                            relief=tk.RAISED, borderwidth=5, background="#808080",command=self.add_user)
        btn_check = tk.Button(master=window, text="Check attendance", width=25, font=("Helvetica", 20),
                              relief=tk.RAISED, borderwidth=5, background="#808080",command=self.check_user)
        btn_amount = tk.Button(master=window, text="Check list", width=25, font=("Helvetica", 20), 
                                relief=tk.RAISED, borderwidth=5,background="#808080")
        btn_exit = tk.Button(master=window, text="Exit", width=25, font=("Helvetica", 20),
                             relief=tk.RAISED, borderwidth=5, background="#808080",command=self.exit_tkinter)
        label = tk.Label(self.logo_bme_frame, image=self.logo_bme)
        label.pack()

        # Position of widget
        self.header.place(relx=0.5, rely=0.05, relwidth=0.7, relheight=0.1, anchor='n')
        self.logo_bme_frame.pack()
        self.logo_bme_frame.place(anchor='center', relx=0.85, rely=0.1)
        btn_add.place(relx=0.05, rely=0.25, relwidth=0.2,
                      relheight=0.1, anchor='nw')
        btn_check.place(relx=0.05, rely=0.4, relwidth=0.2,
                        relheight=0.1, anchor='nw')
        btn_amount.place(relx=0.05, rely=0.55, relwidth=0.2,
                         relheight=0.1, anchor='nw')
        btn_exit.place(relx=0.05, rely=0.7, relwidth=0.2,
                       relheight=0.1, anchor='nw')

        
    def add_user(self):
        self.add_user_window = tk.Toplevel(self.window)
        # self.add_user_window.attributes('-fullscreen', True)
        self.add_user_window.geometry("%dx%d+0+0" % (self.add_user_window.winfo_screenwidth() , self.add_user_window.winfo_screenheight()))
        self.header = tk.Label(master=self.add_user_window, text="Face Recognition App", font=("Helvetica", 40))
        self.logo_bme_add_user = tk.Frame(master=self.add_user_window)
        label = tk.Label(self.logo_bme_add_user, image=self.logo_bme)
        label.pack()
        self.header.place(relx=0.5, rely=0.05, relwidth=0.7, relheight=0.1, anchor='n')
        self.logo_bme_add_user.pack()
        self.logo_bme_add_user.place(anchor='center', relx=0.85, rely=0.1)
        # self.add_user_window.geometry("%dx%d" % (self.add_user_window.winfo_screenwidth() , self.add_user_window.winfo_screenheight()))
        self.params["UPDATE_DATABASES"] = True
        photonic_face_recognition = PhotonicFaceRecognition(**self.params)
        self.entry_string = tk.StringVar()
        entry_input_name = tk.Entry(master=self.add_user_window, textvariable=self.entry_string)
        label_input_name = tk.Label(master=self.add_user_window, text="Input name:", font=("Helvetica", 20))

        def string_enter():
            global input_name
            input_name = self.entry_string.get()
            user_name = copy.deepcopy(input_name)
            return user_name[1:]

        VirtualKeyboardJetson(self.entry_string, self.add_user_window)

        btn_enter = tk.Button(master=self.add_user_window, text="Enter", padx=5, pady=5, font=("Helvetica", 20), 
                                relief=tk.RAISED, borderwidth=5, background="#808080", command=lambda: add_new_student_tkinter(photonic_face_recognition, string_enter(), self.params))# FaceRecognitionTkinter(self.add_user_window, string_enter(), photonic_face_recognition, self.params, FILE_CONFIG).show_camera())
        btn_back_home = tk.Button(master=self.add_user_window, text="Back home", padx=5, pady=5, font=("Helvetica", 20), 
                                  relief=tk.RAISED, borderwidth=5, background="#808080", command=lambda: self.add_user_window.destroy())
        entry_input_name.place(
            relx=0.5, rely=0.2, relwidth=0.5, anchor='n', relheight=0.1)
        label_input_name.place(relx=0.15, rely=0.2,
                               relwidth=0.15, anchor='n', relheight=0.1)
        btn_enter.place(relx=0.95, rely=0.25, relwidth=0.15,
                        anchor='e', relheight=0.1)
        btn_back_home.place(relx=0.95, rely=0.4, relwidth=0.15, 
                        anchor='e', relheight=0.1)


    def check_user(self):
        self.params["UPDATE_DATABASES"] = False
        photonic_face_recognition = PhotonicFaceRecognition(**self.params)
        # face_recognition = FaceRecognitionTkinter(
        #     self.window, None, photonic_face_recognition, self.params, self.file_config)
        # face_recognition.check_attendance()
        check_attendance_opencv(photonic_face_recognition, self.params)
    def exit_tkinter(self):
        # save_inference_config(self.params, self.file_config)
        self.window.destroy()


if __name__ == '__main__':
    window = tk.Tk()
    app = App(window, FILE_CONFIG)
    window.mainloop()
