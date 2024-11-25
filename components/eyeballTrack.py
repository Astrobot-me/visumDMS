import numpy as np
import cv2,time 
from collections import deque
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

class Eyeball:

    def __init__(self):
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        self.LEFT_IRIS = [474, 475, 476, 477]
        self.RIGHT_IRIS = [469, 470, 471, 472]

        # To store iris data
        self.history_length = 50
        self.left_eye_horizontal = deque(maxlen=self.history_length)
        self.left_eye_vertical = deque(maxlen=self.history_length)
        self.right_eye_horizontal = deque(maxlen=self.history_length)
        self.right_eye_vertical = deque(maxlen=self.history_length)

        #Eye ball status 

        self.EYEBALL_ORIENTATION = ['UP','DOWN','LEFT','RIGHT']

    def detectIrisPos(self,iris_landmarks, eye_landmarks):

        iris_center = np.mean(iris_landmarks, axis=0)  # Center of the iris
        left_corner = eye_landmarks[0]
        right_corner = eye_landmarks[3]
        top_corner = eye_landmarks[1]
        bottom_corner = eye_landmarks[5]

        #calculation ratios 
        eye_width = np.linalg.norm(right_corner - left_corner)
        eye_height = np.linalg.norm(top_corner - bottom_corner)
        horizontal_ratio = (iris_center[0] - left_corner[0]) / eye_width
        vertical_ratio = (iris_center[1] - top_corner[1]) / eye_height

        # Determine direction based on the ratios
        horizontal_direction = "Center"
        vertical_direction = "Center"

        if horizontal_ratio < 0.35:
            horizontal_direction = self.EYEBALL_ORIENTATION[2] #"Left"
        elif horizontal_ratio > 0.65:
            horizontal_direction = self.EYEBALL_ORIENTATION[3] # RIGHT

        if vertical_ratio < 0.35:
            vertical_direction = self.EYEBALL_ORIENTATION[0] # up
        elif vertical_ratio > 0.65:
            vertical_direction = self.EYEBALL_ORIENTATION[1] #"Down"

        return horizontal_ratio, vertical_ratio, horizontal_direction, vertical_direction

    def getIrisPos(self,face_landmarks,image):

        height, width, _ = image.shape
        if face_landmarks.multi_face_landmarks:
            for face_landmark in face_landmarks.multi_face_landmarks:
                # Extract landmarks
                landmarks = np.array([[lm.x * width, lm.y * height] for lm in face_landmark.landmark])
                
                left_eye = landmarks[self.LEFT_EYE]
                right_eye = landmarks[self.RIGHT_EYE]
                left_iris = landmarks[self.LEFT_IRIS]
                right_iris = landmarks[self.RIGHT_IRIS]

                # Detect Iris Positions (both ratios and directions)
                left_horizontal, left_vertical, left_horizontal_direction, left_vertical_direction = self.detectIrisPos(left_iris, left_eye)
                right_horizontal, right_vertical, right_horizontal_direction, right_vertical_direction = self.detectIrisPos(right_iris, right_eye)

                # Append to history
                self.left_eye_horizontal.append(left_horizontal)
                self.left_eye_vertical.append(left_vertical)
                self.right_eye_horizontal.append(right_horizontal)
                self.right_eye_vertical.append(right_vertical)

                # Draw eyes and iris for visualization
                for point in self.LEFT_EYE + self.RIGHT_EYE + self.LEFT_IRIS + self.RIGHT_IRIS:
                    cv2.circle(image, (int(landmarks[point][0]), int(landmarks[point][1])), 2, (255, 0, 0), -1)  # Blue Circles

                left_eye = {
                    'lh':left_horizontal,
                    'lv':left_vertical,
                    'lhd':left_horizontal_direction,
                    'lvd':left_vertical_direction
                }

                right_eye = {
                    'rh':left_horizontal,
                    'rv':left_vertical,
                    'rhd':left_horizontal_direction,
                    'rvd':left_vertical_direction
                }
            
        return left_eye,right_eye

        



