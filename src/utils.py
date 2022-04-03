import numpy as np
import json
import os
import cv2
import time
import sys
import tkinter as tk
import cv2
from PIL import Image, ImageTk

class MyVideoCapture:
     def __init__(self, video_source=0):
         # Open the video source
         self.vid = cv2.VideoCapture(video_source)
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)
 
         # Get video source width and height
         self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
         self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
 
     def get_frame(self):
         if self.vid.isOpened():
             ret, frame = self.vid.read()
             if ret:
                 # Return a boolean success flag and the current frame converted to BGR
                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
             else:
                 return (ret, None)
         else:
             return (ret, None)
 
     # Release the video source when the object is destroyed
     def __del__(self):
         if self.vid.isOpened():
             self.vid.release()

class FaceRecognitionTkinter:
    """Class use for graphical user interface (GUI) by using Tkinter library. 
    Include 3 functions (state: Updating):
    - show_camera (Add user) -> snapshot_clicked
    - check_attendance

    Args:
    - window <object>: object of Tkinter
    - entry_input_name <string>: name of user
    - photonic_face_recognition <object>: object of PhotonicFaceRecognition class
    - params <dict>: parameters json format
    - FILE_CONFIG <string>: path of config file
    """
    def __init__(self, window, entry_input_name, photonic_face_recognition, params, FILE_CONFIG):
        self.window = window
        self.file_config = FILE_CONFIG
        self.photonic_face_recognition = photonic_face_recognition
        self.user = entry_input_name
        self.params = params
        self.process_this_frame = True
        self.video_capture = MyVideoCapture(0)
        if self.user is not None:
            self.params["CLASSES"].append(self.user)

        
    def snapshot_clicked(self):
        """Auto save face image and encode. Then add user into parameter CLASSES of config"""
        if self.flag == "Correct":
            if len(self.face_locations) > 1:
                self.label_notification = tk.Label(master=self.window, text="Detected more 1 faces in image, please make sure just 1 face in image")
            else:
                save_inference_config(self.params, self.file_config)
                update_face_image(self.frame_clone, self.face_locations, self.params, self.user)
                # update_face_embed_vector(photonic_face_recognition, face_locations, params, name_student)
                known_face_encodings, known_face_names = self.photonic_face_recognition.load_ground_truth_face_image_samples()
                self.params["CLASSES"] = known_face_names
        
                # save new embedded vector of new instance in `face-embedded-vector`.
                save_face_embed_vector(self.params["TXT_FILE_DIR"], known_face_encodings, known_face_names)
                self.label_notification = tk.Label(master=self.window, text="Saved into database successful")
        else:
            self.label_notification = tk.Label(master=self.window, text="Please move your face in the middle camera")
        self.label_notification.place(relx=0.35, rely=0.9, relwidth=0.2, anchor='n', relheight=0.1)


    def show_camera(self):
        """Show camera and detect human face"""
        label_hello_user = tk.Label(master=self.window, text="Hello {}".format(self.user))
        label_show_camera = tk.Label(master=self.window, width=self.video_capture.width, height=self.video_capture.height)

        label_show_camera.place(relx=0.35, rely=0.4)
        label_hello_user.place(relx=0.35, rely=0.3, relwidth=0.2, anchor='n', relheight=0.1)
        # Grab a single frame of video
        _, frame = self.video_capture.get_frame()
        
        # Frame_clone is frame but not be affected by drawning
        self.frame_clone = frame.copy()
        self.frame_clone = cv2.cvtColor(self.frame_clone, cv2.COLOR_BGR2RGB)

        # Down scale frame
        small_frame = self.photonic_face_recognition.down_scale_image(frame, self.params["DOWN_SCALE"])

        # Apply trick to increase FPS
        if self.process_this_frame:
            self.face_locations = self.photonic_face_recognition.face_detection_algorithm(small_frame)
        
        # turn flag of process frame, mean if first frame is processed, second frame is not, third frame is processed, etc.
        self.process_this_frame = not self.process_this_frame

        # Draw frame
        self.flag = self.photonic_face_recognition.face_detection_drawing(frame, self.face_locations, self.params["DOWN_SCALE"])

        frame_PIL = Image.fromarray(frame)
        frame_tk = ImageTk.PhotoImage(image=frame_PIL)
        label_show_camera.imgtk = frame_tk
        label_show_camera.configure(image=frame_tk)
        label_show_camera.after(10, self.show_camera)

    def check_attendance(self):
        """Detect human face and classify name of user in CLASSES"""
        label_note = tk.Label(master=self.window, text="Note: Please fix your face in front of the camera for 1 second for attendance")
        label_note.place(relx=0.35, rely=0.33)
        label_check_attendance = tk.Label(master=self.window, width=self.video_capture.width, height=self.video_capture.height)
        label_check_attendance.place(relx=0.35, rely=0.4)

        # Load available instances in dataset.
        known_face_names = self.params["CLASSES"]
        known_face_encodings = self.photonic_face_recognition.load_know_face_encodings(self.params["TXT_FILE_DIR"], known_face_names)

        # Grab a single frame of video
        _, frame = self.video_capture.get_frame()

        # down scale frame
        small_frame = self.photonic_face_recognition.down_scale_image(frame, self.params["DOWN_SCALE"])

        # Apply trick to increase FPS
        if self.process_this_frame:
            self.face_locations = self.photonic_face_recognition.face_detection_algorithm(small_frame)
            self.face_encodings = self.photonic_face_recognition.face_encoding_algorithm(small_frame, self.face_locations)
            self.face_names = self.photonic_face_recognition.face_recognition_algorithm(self.face_encodings, known_face_encodings, 
                                                                            known_face_names, self.params["TOLERANCE"])
        
        # turn flag of process frame, mean if first frame is processed, second frame is not, third frame is processed, etc.
        self.process_this_frame = not self.process_this_frame

        # Draw frame
        self.photonic_face_recognition.face_recognition_drawning(frame, self.face_locations, self.face_names, self.params["DOWN_SCALE"])
        frame_PIL = Image.fromarray(frame)
        frame_tk = ImageTk.PhotoImage(image=frame_PIL)
        label_check_attendance.imgtk = frame_tk
        label_check_attendance.configure(image=frame_tk)
        label_check_attendance.after(10, self.check_attendance)

### UTILITIES FUNCTION FOR `src/photonic_face_recognition`.
def update_config(params, known_face_names):
    params["CLASSES"] = known_face_names

def save_inference_config(params, file_save_json):
    with open(file_save_json, 'w') as file:
        json.dump(params, file)

def save_face_embed_vector(txt_file_dir, known_face_encodings, known_face_names):
    for i in range(len(known_face_encodings)):
        know_face_encoding = known_face_encodings[i]
        known_face_name = known_face_names[i]
        known_face_name = known_face_name.replace(' ', '_')
        np.savetxt(os.path.join(txt_file_dir, known_face_name + ".txt"), know_face_encoding, delimiter = '\n')

def update_face_embed_vector(photonic_face_recognition, face_locations, params, name_file):
    ground_truth = photonic_face_recognition.load_ground_truth_image(name_file.replace(' ', '_') + ".png")
    face_encoding = photonic_face_recognition.face_encoding_algorithm(ground_truth, face_locations)[0]
    face_encodings_file = os.path.join(params["TXT_FILE_DIR"], name_file.replace(' ', '_') + ".txt")
    np.savetxt(face_encodings_file, face_encoding, delimiter = '\n')
    print(f"Done saved embedded face vector of {name_file} in {face_encodings_file}")

def update_face_image(input_image, face_locations, params, name_file):
    ''' save face image when open camera. Use for `add new student` event
    Args:
        + input_image (ndarray): Image array with shape (H, C, 3) with 3 represent to RGB.
                                 If use OpenCV to read image, you must convert from BGR to RGB before.
        + face_locations (list(ndarray)): List contains all offset value (top, right, bottom, left) of face locations in image.
        + params (dict): dictionary is loaded by config file.
        + name_file (string): name file without extendsion file.          
    '''

    # get offset value 
    top, right, bottom, left = face_locations[0]
    if params["DOWN_SCALE"]:
        # Scale back up face locations since the frame we detected in was scaled to 1/down_scale size
        top *= params["DOWN_SCALE"]
        right *= params["DOWN_SCALE"]
        bottom *= params["DOWN_SCALE"]
        left *= params["DOWN_SCALE"]

    # Expand face image to save.
    top -= 60
    right += 60
    bottom += 60
    left -= 60 
    
    face_image = input_image[top:bottom, left:right]
    face_image_file = os.path.join(params["IMAGE_PATH"], name_file.replace(' ', '_') + ".png")
    cv2.imwrite(face_image_file, face_image)
    print(f"Done saved face image of {name_file} in {face_image_file}")

### UTILITIES FUNCTION FOR `app_opencv.py`
def draw_fps_opencv(frame, fps):
    frame = cv2.putText(frame, f"FPS: {fps}", (0, 30), cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 0, 255), 1)

    return frame

def add_new_student_opencv(photonic_face_recognition, params):
    '''function is used for `Add new student` event'''

    name_student = input("Please enter name of new student: ")
    params["CLASSES"].append(name_student)
    print(f"Hello {name_student}")
    # setup 
    prev_frame_time = 0
    new_frame_time = 0
    video_capture = cv2.VideoCapture(0)
    process_this_frame = True
    while True:
        # Grab a single frame of video
        _, frame = video_capture.read()
        
        # frame_clone is frame but not be affected by drawning
        frame_clone = frame.copy()

        # down scale frame
        small_frame = photonic_face_recognition.down_scale_image(frame, params["DOWN_SCALE"])

        # convert frame to RGB
        rgb_small_frame = small_frame[:, :, ::-1]

        # Apply trick to increase FPS
        if process_this_frame:
            face_locations = photonic_face_recognition.face_detection_algorithm(rgb_small_frame)
        
        # turn flag of process frame, mean if first frame is processed, second frame is not, third frame is processed, etc.
        process_this_frame = not process_this_frame

        # Draw frame
        flag = photonic_face_recognition.face_detection_drawing(frame, face_locations, params["DOWN_SCALE"])

        # calculate FPS
        new_frame_time = time.time()
        fps = int(1 / (new_frame_time - prev_frame_time))
        draw_fps_opencv(frame, fps)
        prev_frame_time = new_frame_time
        
        # Display the resulting image
        cv2.imshow('Video', frame)
        key = cv2.waitKey(1)
        
        # press ENTER
        if key == 13:
            if flag == "Correct":
                if len(face_locations) > 1:
                     print(f"Detected more 1 faces in image, please make sure just 1 face in image")
                else:
                    update_face_image(frame_clone, face_locations, params, name_student)

                    # update_face_embed_vector(photonic_face_recognition, face_locations, params, name_student)
                    known_face_encodings, known_face_names = photonic_face_recognition.load_ground_truth_face_image_samples()
                    params["CLASSES"] = known_face_names
            
                    # save new embedded vector of new instance in `face-embedded-vector`.
                    save_face_embed_vector(params["TXT_FILE_DIR"], known_face_encodings, known_face_names)
                    break
            else:
                print("Please move your face in the middle camera")

        # close all if press ESC
        if key == 27:
            break
    
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

def check_attendance_opencv(photonic_face_recognition, params):
    '''Function is used for `Check attendance` envent'''

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
            face_locations = photonic_face_recognition.face_detection_algorithm(rgb_small_frame)
            face_encodings = photonic_face_recognition.face_encoding_algorithm(rgb_small_frame, face_locations)
            face_names = photonic_face_recognition.face_recognition_algorithm(face_encodings, known_face_encodings, 
                                                                              known_face_names, params["TOLERANCE"])
        
        # turn flag of process frame, mean if first frame is processed, second frame is not, third frame is processed, etc.
        process_this_frame = not process_this_frame

        # Draw frame
        photonic_face_recognition.face_recognition_drawning(frame, face_locations, face_names, params["DOWN_SCALE"])

        # calculate FPS
        new_frame_time = time.time()
        fps = int(1 / (new_frame_time - prev_frame_time))
        draw_fps_opencv(frame, fps)
        prev_frame_time = new_frame_time
        
        # Display the resulting image
        cv2.imshow('Video', frame)
        key = cv2.waitKey(1)

        # close all if press ESC
        if key == 27:
            break
    
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
