import numpy as np
import os
from pathlib import Path
import face_recognition
import cv2
import sys

class SettingConfig(object):
    def __init__(self, **args):
        for key in args:
            setattr(self, key, args[key])
            
class PhotonicFaceRecognition(SettingConfig):
    def __init__(self, **args):
        super(PhotonicFaceRecognition, self).__init__(**args)
    
    def load_ground_truth_face_image_samples(self):
        ''' Load all ground truth images in face-image-samples folders and encoding it.

        Returns:
        + known_face_encodings (list(ndarray)): List with length = N (N Number of samples) 
                                                contains embedded vectore with shape (128,).
        + known_face_names (list(string)): List with length = N, contains all names corresponding 
                                           to embedded vector.
        '''

        face_img_files = os.listdir(self.IMAGE_PATH)
        known_face_encodings = []
        known_face_names = []
        for face_img_file in face_img_files:
            face_image_name = Path(face_img_file).stem
            globals()[f"{face_image_name}_encoding"] = face_recognition.face_encodings(
                                                            face_recognition.load_image_file(
                                                                os.path.join(self.IMAGE_PATH, 
                                                                    face_img_file)))[0]
            known_face_encodings.append(globals()[f"{face_image_name}_encoding"])
            known_face_names.append(face_image_name.replace('_', ' '))
        
        return known_face_encodings, known_face_names
    
    def load_know_face_encodings(self, txt_file_dir, known_face_names):
        ''' Load `know_face_encodings (list(ndarray))` contains embedded vectors 
            with shape (128,) by txt file in TXT_FILE_DIR in `config/inference.json`.
        
        Args:
            + txt_file_dir (string): Directory of emmbedded vector txt files.
            + known_face_names (list(string)): List with length = N, contains all lable name 
                                               in CLASSES in `config/inference.json`.
            
        Return:
            + known_face_encodings (list(ndarray)).
        '''

        known_face_encodings = []
        for i in range(len(known_face_names)):
            known_face_name = known_face_names[i]
            encoding_file = known_face_name.replace(' ', '_') + ".txt"
            known_face_encoding = np.loadtxt(os.path.join(txt_file_dir, encoding_file))
            known_face_encodings.append(known_face_encoding)
        
        return known_face_encodings
    
    def down_scale_image(self, input_image, down_scale=4):
        '''Resize frame of video to 1/down_scale size for faster face recognition processing
        Args:
            + input_image (ndarray): Image array with shape (H, C, 3) with 3 represent to RGB.
                                     If use OpenCV to read image, you must convert from BGR to RGB before.
            + down_scale (int): Down scale value, the image is down scaled with 1/down_scale.

        Return:
            + small_input_image (ndarray): Image after down scale.
        '''
        
        small_input_image = cv2.resize(input_image, (0, 0), fx = 1/down_scale, fy = 1/down_scale)

        return small_input_image
    
    def load_ground_truth_image(self, ground_truth_image):
        return face_recognition.load_image_file(os.path.join(self.IMAGE_PATH, ground_truth_image))

    def face_recognition_algorithm(self, face_encodings, known_face_encodings, known_face_names, threshold):
        ''' Face recognition algorithm to recognize all face names object in individual image.
        Args:
            + face_encodings (list(array)): List with length = M (M is number of face object in image) contains 
                                            M 128D embedded vectors.
            + known_face_encodings (list(ndarray)).
            + known_face_names (list(string)).
            + threshold (float): Threshold of algorithm. If use l2/l1 norm it's tolerance.
            + method (string): l2_norm by default.
        
        Return:
            + face_names (list(string)): List contain all predictive name in image.
        '''

        face_names = []
        for face_encoding in face_encodings:
            pred_name = self.similarity_algorithm(known_face_encodings, known_face_names, face_encoding, 
                                                  threshold, self.METHOD_SIMILARITY)
            face_names.append(pred_name)

        return face_names
    
    def face_recognition_drawning(self, input_image, face_locations, face_names, down_scale=4):
        '''Drawing rectangle and predictive name `pred_name` in input image
        Args: 
            + input_image (ndarray): Image array with shape (H, C, 3) with 3 represent to RGB.
                                     If use OpenCV to read image, you must convert from BGR to RGB before.
            + face_locations (list(ndarray)): List contains all offset value (top, right, bottom, left) of face locations in image.
            + face_names (list(string)): List contain all predive name of face objects in image. The oder corresponding to face_locations.
            + down_scale (int): Down scale value. It is down scale value in `down_scale_image` method. 
                                It use to revese offset value with correct with original image.
        '''

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            if down_scale:
                # Scale back up face locations since the frame we detected in was scaled to 1/down_scale size
                top *= down_scale
                right *= down_scale
                bottom *= down_scale
                left *= down_scale

            # Draw a box around the face
            cv2.rectangle(input_image, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(input_image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(input_image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    def face_detection_algorithm(self, input_image):
        ''' Face detection algorithm
        Args: 
            + input_image (ndarray): Image array with shape (H, C, 3) with 3 represent to RGB.
                                     If use OpenCV to read image, you must convert from BGR to RGB before.
        
        Returns:
            + face_locations (list(ndarray)): List contains all offset value (top, right, bottom, left) of face locations in image.
        '''

        # Applied HOG + SVM to face detection in image.
        face_locations = face_recognition.face_locations(input_image)
        
        return face_locations

    def face_encoding_algorithm(self, input_image, face_locations):
        ''' Face encoding algorithm to encoding all face object in individual image
        Args:
            + input_image (ndarray): Image array with shape (H, C, 3) with 3 represent to RGB.
                                     If use OpenCV to read image, you must convert from BGR to RGB before.
            + + face_locations (list(ndarray)): List contains all offset value (top, right, bottom, left) of face locations in image.
        
        return:
            + face_encodings (list(array)): List with length = M (M is number of face object in image) contains 
                                            M 128D embedded vectors.
        '''

        # Applied dlib_face_recognition_resnet_model_v1 to encoding face object in image.
        # https://github.com/davisking/dlib-models#dlib_face_recognition_resnet_model_v1datbz2
        face_encodings = face_recognition.face_encodings(input_image, face_locations)

        return face_encodings

    def similarity_algorithm(self, known_face_encodings, known_face_names, face_encoding, threshold, method="l2_norm"):
        ''' Similarity algorithm to calculate the similarity score of each object in image.
            Mean if in input image has more 1 face object, this algorithms is applied to process
            each object `face_encoding`.
        Args:
            + known_face_encodings (list(ndarray)).
            + known_face_names (list(string)).
            + face_encoding (ndarray): 128D embedded vector of single face.
            + threshold (float): Threshold of algorithm. If use l2/l1 norm it's tolerance.
            + method (string): l2_norm by default. 
        
        return: pred_name (string): Predictive name in CLASSES `config/inference.json`. 
                If the similarity score do not satisfy with threshold (like L2 norm >= tolerance)
                then pred_name is `Unkown`.
        '''

        if method == "l2_norm":
            threshold = self.TOLERANCE
            pred_name = self._l2_norm_algorithm(known_face_encodings, known_face_names, face_encoding, threshold)
        
        return pred_name
    
    def _l2_norm_algorithm(self, known_face_encodings, known_face_names, face_encoding, tolerance):
        ''' Apply L2 norm for Similarity algorithm.

        Return: 
            pred_name (string): Predictive name in CLASSES `config/inference.json`.
                                If min_face_distance >= tolerance then pred_name is `Unknown`.
        '''

        face_distances = np.linalg.norm(known_face_encodings - face_encoding, axis = 1)
        min_face_distance = face_distances[np.argmin(face_distances)]
        if min_face_distance < tolerance:
            min_face_distance_index = list(face_distances).index(min_face_distance)
            pred_name = known_face_names[min_face_distance_index]
        else:
            pred_name = "Unknown"
        
        return pred_name
    
    def face_detection_drawing(self, input_image, face_locations, down_scale=4):
        ''' Drawing face detection (red rectange) and splitted image (blue rectangle).
            This function is applied for `Add new student` event.
        '''

        image_h, image_w = input_image.shape[:2]
        flag = "Invalid"
        for (top, right, bottom, left) in face_locations:
            if down_scale:
                # Scale back up face locations since the frame we detected in was scaled to 1/down_scale size
                top *= down_scale
                right *= down_scale
                bottom *= down_scale
                left *= down_scale

            # Draw a box around the face
            cv2.rectangle(input_image, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(input_image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(input_image, "Human face", (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Draw a rectangle that will be splited and save it into database
            top -= 60
            right += 60
            bottom += 60
            left -= 60 

            if (top < 0) | (left < 0) | (right > image_w) | (bottom > image_h):
                flag = "Incorrect"
            else:
                flag = "Correct"
            cv2.rectangle(input_image, (left, top), (right, bottom), (255, 0, 0), 2)
            cv2.rectangle(input_image, (left, top - 35), (right, top), (255, 0, 0), cv2.FILLED)
            cv2.putText(input_image, flag, (left + 6, top - 6), font, 1.0, (255, 255, 255), 1)

        return flag

    
