import numpy as np
import json
import os
import cv2
import time
import platform
import cv2


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

class Button(object):
    def __init__(self, text, x, y, width, height, command=None):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.left = 10
        self.top  = 10
        #self.right  = x + width - 1 
        self.right = 100
        self.bottom = 60
        
        self.hover = False
        self.clicked = False
        self.command = command
        
    def exit_event(self, event, x, y, flags, param):
        self.hover = (self.left <= x <= self.right and \
            self.top <= y <= self.bottom)
            
        if self.hover and flags == 1:
            self.clicked = False
            global running
            running = False
            if self.command:
                self.command()
        
        
    def draw_exit(self, frame):
        if not self.hover:
            
            #cv2.circle(frame, (20,20), 10 , (0,0,255), -1)
            cv2.rectangle(frame, (10,10), (100,60), (0,0,255), -1)
            cv2.putText(frame, "Exit", (20,40), cv2.FONT_HERSHEY_PLAIN, 2 , (255,255,255), 2)
        else:
            cv2.rectangle(frame, (10,10), (100,60), (0,255,0), -1)
            cv2.putText(frame, "Exit", (20,40), cv2.FONT_HERSHEY_PLAIN, 2 , (255,255,255), 2)
    
    

def add_new_student_opencv(photonic_face_recognition, params):
    '''function is used for `Add new student` event'''

    name_student = input("Please enter name of new student: ")
    params["CLASSES"].append(name_student)
    print(f"Hello {name_student}")
    
    # setup 
    button = Button('QUIT', 0, 0, 100, 30)
    prev_frame_time = 0
    new_frame_time = 0
    video_capture = video_capture_mul_platform()
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
    global running
    running = True
    '''Function is used for `Check attendance` envent'''

    # Load avaiable instances in dataset.
    known_face_names = params["CLASSES"]
    known_face_encodings = photonic_face_recognition.load_know_face_encodings(params["TXT_FILE_DIR"], known_face_names)

    # setup 
    button = Button('QUIT', 0, 0, 100, 30)
    prev_frame_time = 0
    new_frame_time = 0
    video_capture = video_capture_mul_platform()
    patiences = params["PATIENCES"]
    i = patiences
    prev_face_name = None
    check_atten_count = 0
    while running:
        # Grab a single frame of video
        _, frame = video_capture.read()

        # down scale frame
        small_frame = photonic_face_recognition.down_scale_image(frame, params["DOWN_SCALE"])

        # convert frame to RGB
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # process_this_frame
        if (i == patiences):
            # face dectection
            face_locations = photonic_face_recognition.face_detection_algorithm(rgb_small_frame)
            if len(face_locations) == 1:
                # encoding face
                face_encodings = photonic_face_recognition.face_encoding_algorithm(rgb_small_frame, face_locations)
                
                # face recognition
                face_names = photonic_face_recognition.face_recognition_algorithm(face_encodings, known_face_encodings, 
                                                                                  known_face_names, params["TOLERANCE"])
                if prev_face_name is None:
                    prev_face_name = face_names[0]
                else:
                    cur_face_name = face_names[0]
                    if prev_face_name == cur_face_name:
                        check_atten_count += 1
                    # if different face then reset 
                    else:
                        check_atten_count = 0
                        prev_face_name = None

            # if find 2 faces then rest
            else:
                check_atten_count = 0
                prev_face_name = None
                face_names = ["people" for _ in range(len(face_locations))]
            
            # reset value of i
            i = 1
        else:
            i += 1

        # Draw frame
        photonic_face_recognition.face_recognition_drawning(frame, face_locations, face_names, params["DOWN_SCALE"])

        # calculate FPS
        new_frame_time = time.time()
        fps = int(1 / (new_frame_time - prev_frame_time))
        if params["DRAW_FPS"]:
            draw_fps_opencv(frame, fps)
        prev_frame_time = new_frame_time
        
        # Draw button
        button.draw_exit(frame)
        
        # Display the resulting image
        cv2.imshow('Video', frame)

        # set mouse clicl
        cv2.setMouseCallback("Video", button.exit_event)

        key = cv2.waitKey(1)

        # close all if press ESC
        if key == 27:
            running = False
        if check_atten_count == params["ATTENDANCE_THR"]:
            print(f"Hello {cur_face_name}")
            running = False
    
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

def _compute_iou(bbox_1, bbox_2):
    '''
    Args:
        + bbox_1: (list) with shape (4, ) contain (x_min, y_min, x_max, y_max)
        + bbox_2: (list) with shape (4, ) contain (x_min, y_min, x_max, y_max)
    Output:
        + iou (float) Intersection over Union of both bboexs.
    '''
    
    assert bbox_1[0] < bbox_1[2], "invalid format"
    assert bbox_1[1] < bbox_1[3], "invalid format"
    assert bbox_2[0] < bbox_2[2], "invalid format"
    assert bbox_2[1] < bbox_2[3], "invalid format"

    # determine the coordinates of the intersection rectangle
    x_left = max(bbox_1[0], bbox_2[0])
    x_right = min(bbox_1[2], bbox_2[2])
    y_top = max(bbox_1[1], bbox_2[1])
    y_bottom = min(bbox_1[3], bbox_2[3])
    if (x_left >= x_right) or (y_top >= y_bottom):
        iou = -1
    else:
        # compute intersection area
        intersection_area = (x_right - x_left) * (y_bottom - y_top)

        # compute area of 2 bboxes
        bbox_1_area = (bbox_1[2] - bbox_1[0]) * (bbox_1[3] - bbox_1[1])
        bbox_2_area = (bbox_2[2] - bbox_2[0]) * (bbox_2[3] - bbox_2[1])
        try:
            # compute iou
            # might be prevent some case iou < 0 or iou > 1 --> but in chest_xray we don't need
            iou = intersection_area / float(bbox_1_area + bbox_2_area - intersection_area)
        except ZeroDivisionError:
            iou = -1
    
    return iou

### JETSON NANO CONFIGURE
def _running_on_jetson_nano():
    # To make the same code work on a laptop or on a Jetson Nano, we'll detect when we are running on the Nano
    # so that we can access the camera correctly in that case.
    # On a normal Intel laptop, platform.machine() will be "x86_64" instead of "aarch64"
    return platform.machine() == "aarch64"

def _get_jetson_gstreamer_source(capture_width=1280, capture_height=720, display_width=1280, display_height=720, framerate=60, flip_method=1):
    """
    Return an OpenCV-compatible video source description that uses gstreamer to capture video from the camera on a Jetson Nano
    """
    return (
            f'nvarguscamerasrc ! video/x-raw(memory:NVMM), ' +
            f'width=(int){capture_width}, height=(int){capture_height}, ' +
            f'format=(string)NV12, framerate=(fraction){framerate}/1 ! ' +
            f'nvvidconv flip-method={flip_method} ! ' +
            f'video/x-raw, width=(int){display_width}, height=(int){display_height}, format=(string)BGRx ! ' +
            'videoconvert ! video/x-raw, format=(string)BGR ! appsink'
            )

def video_capture_mul_platform():
    if _running_on_jetson_nano():
        # Accessing the camera with OpenCV on a Jetson Nano requires gstreamer with a custom gstreamer source string
        video_capture = cv2.VideoCapture(_get_jetson_gstreamer_source(), cv2.CAP_GSTREAMER)
    else:
        # Accessing the camera with OpenCV on a laptop just requires passing in the number of the webcam (usually 0)
        video_capture = cv2.VideoCapture(0)
    
    return video_capture

