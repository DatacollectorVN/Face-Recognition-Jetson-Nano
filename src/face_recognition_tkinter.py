import cv2
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from src.utils import save_face_embed_vector, save_inference_config, update_face_image, video_capture_mul_platform

class MyVideoCapture:
     def __init__(self):
         # Open the video source
         self.vid = video_capture_mul_platform() # TO DO: cv2.VideoCapture(0)
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source")
 
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
        self.video_capture = MyVideoCapture()
        if self.user is not None:
            self.params["CLASSES"].append(self.user)

        
    def snapshot_clicked(self):
        """Auto save face image and encode. Then add user into parameter CLASSES of config"""
        if self.flag == "Correct":
            if len(self.face_locations) > 1:
                self.label_notification = tk.Label(master=self.window, text="Detected more 1 faces in image, please make sure just 1 face in image", font=("Helvetica", 20))
            else:
                update_face_image(self.frame_clone, self.face_locations, self.params, self.user)
                # update_face_embed_vector(photonic_face_recognition, face_locations, params, name_student)
                known_face_encodings, known_face_names = self.photonic_face_recognition.load_ground_truth_face_image_samples()
                self.params["CLASSES"] = known_face_names
        
                # save new embedded vector of new instance in `face-embedded-vector`.
                save_face_embed_vector(self.params["TXT_FILE_DIR"], known_face_encodings, known_face_names)
                self.label_notification = tk.Label(master=self.window, text="Saved into database successful", font=("Helvetica", 20))
        else:
            self.label_notification = tk.Label(master=self.window, text="Please move your face in the middle camera", font=("Helvetica", 20))
        self.label_notification.place(relx=0.35, rely=0.9, relwidth=0.2, anchor='n', relheight=0.1)


    def show_camera(self):
        """Show camera and detect human face"""
        label_hello_user = tk.Label(master=self.window, text="Hello {}".format(self.user), font=("Helvetica", 20))
        # label_show_camera = tk.Label(master=self.window, width=self.video_capture.width, height=self.video_capture.height)
        label_show_camera = tk.Canvas(master=self.window, width = self.video_capture.width, height = self.video_capture.height)
        label_show_camera.place(relx=0.35, rely=0.4)

        # label_show_camera.place(relx=0.15, rely=0.4)
        label_hello_user.place(relx=0.2, rely=0.3, relwidth=0.2, anchor='n', relheight=0.1)
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
        # label_show_camera.imgtk = frame_tk
        # label_show_camera.configure(image=frame_tk)
        # label_show_camera.after(10, self.show_camera)
        label_show_camera.create_image(0, 0, anchor=tk.NW, image=frame_tk)
        label_show_camera.after(1, self.show_camera)

    def check_attendance(self):
        """Detect human face and classify name of user in CLASSES"""
        label_note = tk.Label(master=self.window, text="Note: Please fix your face in front of the camera for 1 second for attendance", font=("Helvetica", 12))
        label_note.place(relx=0.35, rely=0.33)
        # label_check_attendance = tk.Label(master=self.window, width=self.video_capture.width, height=self.video_capture.height)
        # label_check_attendance.place(relx=0.35, rely=0.4)
        label_check_attendance = tk.Canvas(master=self.window, width = self.video_capture.width, height = self.video_capture.height)
        label_check_attendance.place(relx=0.35, rely=0.4)

        # Load available instances in dataset.
        known_face_names = self.params["CLASSES"]
        known_face_encodings = self.photonic_face_recognition.load_know_face_encodings(self.params["TXT_FILE_DIR"], known_face_names)

        # Setup
        patiences = self.params["PATIENCES"]
        i = patiences

        # Grab a single frame of video
        _, frame = self.video_capture.get_frame()

        # down scale frame
        small_frame = self.photonic_face_recognition.down_scale_image(frame, self.params["DOWN_SCALE"])

        # Apply trick to increase FPS
        if (i == patiences):
            self.face_locations = self.photonic_face_recognition.face_detection_algorithm(small_frame)
            self.face_encodings = self.photonic_face_recognition.face_encoding_algorithm(small_frame, self.face_locations)
            self.face_names = self.photonic_face_recognition.face_recognition_algorithm(self.face_encodings, known_face_encodings, 
                                                                            known_face_names, self.params["TOLERANCE"])
            # reset value of i
            i = 1
        else:
            i += 1
        # turn flag of process frame, mean if first frame is processed, second frame is not, third frame is processed, etc.
        self.process_this_frame = not self.process_this_frame

        # Draw frame
        self.photonic_face_recognition.face_recognition_drawning(frame, self.face_locations, self.face_names, self.params["DOWN_SCALE"])
        frame_PIL = Image.fromarray(frame)
        frame_tk = ImageTk.PhotoImage(image=frame_PIL)
        label_check_attendance.imgtk = frame_tk
        # label_check_attendance.configure(image=frame_tk)
        # label_check_attendance.after(10, self.check_attendance)
        label_check_attendance.create_image(0, 0, anchor=tk.NW, image=frame_tk)
        label_check_attendance.after(1, self.check_attendance)

        