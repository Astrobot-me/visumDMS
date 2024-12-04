import numpy as np
import cv2
from typing import List, Dict, Tuple


class Eyeball:
    def __init__(self):
        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        self.LEFT_IRIS = [474, 475, 476, 477]
        self.RIGHT_IRIS = [469, 470, 471, 472]


        # Eye ball status
        self.EYEBALL_ORIENTATION = ['UP', 'DOWN', 'LEFT', 'RIGHT']

        #
        self.horizontal_threshold = 0.3
        self.vertical_threshold = 0.3
        self.time_window = 5
        
        # Movement tracking
        self.horizontal_history = []
        self.vertical_history = []

    def detectIrisPos(self, iris_landmarks, eye_landmarks):
        try:
            iris_center = np.mean(iris_landmarks, axis=0)  # Center of the iris
            left_corner = eye_landmarks[0]
            right_corner = eye_landmarks[3]
            top_corner = eye_landmarks[1]
            bottom_corner = eye_landmarks[5]

            # Calculate ratios
            eye_width = np.linalg.norm(right_corner - left_corner)
            eye_height = np.linalg.norm(top_corner - bottom_corner)

            if eye_width == 0 or eye_height == 0:
                raise ValueError("Eye width or height is zero; cannot compute ratios.")

            horizontal_ratio = (iris_center[0] - left_corner[0]) / eye_width
            vertical_ratio = (iris_center[1] - top_corner[1]) / eye_height

            # Determine direction based on the ratios
            horizontal_direction = "Center"
            vertical_direction = "Center"

            if horizontal_ratio < 0.35:
                horizontal_direction = self.EYEBALL_ORIENTATION[2]  # "Left"
            elif horizontal_ratio > 0.65:
                horizontal_direction = self.EYEBALL_ORIENTATION[3]  # "Right"

            if vertical_ratio < 0.35:
                vertical_direction = self.EYEBALL_ORIENTATION[0]  # "Up"
            elif vertical_ratio > 0.65:
                vertical_direction = self.EYEBALL_ORIENTATION[1]  # "Down"

            return horizontal_ratio, vertical_ratio, horizontal_direction, vertical_direction
        except Exception as e:
            print(f"Error in detectIrisPos: {e}")
            return "UNREL_DATA", "UNREL_DATA", "UNREL_DATA", "UNREL_DATA"

    def getIrisPos(self, face_landmarks, image):
        try:
            height, width, _ = image.shape

            if not face_landmarks or not face_landmarks.multi_face_landmarks:
                 default_eye_data = {
                'lh': "LMK_AB",
                'lv': "LMK_AB",
                'lhd': "LMK_AB",
                'lvd': "LMK_AB"
                }
                 return default_eye_data,default_eye_data

            for face_landmark in face_landmarks.multi_face_landmarks:
                # Extract landmarks
                landmarks = np.array([[lm.x * width, lm.y * height] for lm in face_landmark.landmark])

                # Handle potential index errors
                try:
                    left_eye = landmarks[self.LEFT_EYE]
                    right_eye = landmarks[self.RIGHT_EYE]
                    left_iris = landmarks[self.LEFT_IRIS]
                    right_iris = landmarks[self.RIGHT_IRIS]
                except IndexError as e:
                    print(f"IndexError: {e}")
                    raise ValueError("Landmark indices out of range.")

                # Detect Iris Positions (both ratios and directions)
                left_horizontal, left_vertical, left_horizontal_direction, left_vertical_direction = self.detectIrisPos(
                    left_iris, left_eye
                )
                right_horizontal, right_vertical, right_horizontal_direction, right_vertical_direction = self.detectIrisPos(
                    right_iris, right_eye
                )

                # Draw eyes and iris for visualization
                for point in self.LEFT_EYE + self.RIGHT_EYE + self.LEFT_IRIS + self.RIGHT_IRIS:
                    cv2.circle(image, (int(landmarks[point][0]), int(landmarks[point][1])), 2, (255, 0, 0), -1)  # Blue Circles

                left_attention = self.update_eye_movement(left_horizontal_direction,left_vertical_direction)
                right_attention = self.update_eye_movement(right_horizontal_direction,right_vertical_direction)

                left_eye_data = {
                    'lh': left_horizontal,
                    'lv': left_vertical,
                    'lhd': left_horizontal_direction,
                    'lvd': left_vertical_direction,
                    'attention':left_attention
                }

                right_eye_data = {
                    'rh': right_horizontal,
                    'rv': right_vertical,
                    'rhd': right_horizontal_direction,
                    'rvd': right_vertical_direction,
                    'attention':right_attention

                }

                return left_eye_data, right_eye_data

        except (ValueError, AttributeError) as e:
            print(f"Error in getIrisPos: {e}")
            default_eye_data = {
                'lh': "UNREL_DATA",
                'lv': "UNREL_DATA",
                'lhd': "UNREL_DATA",
                'lvd': "UNREL_DATA",
                'attention':"UNREL_DATA"
            }
            return default_eye_data, default_eye_data
        except Exception as e:
            print(f"Unexpected error in getIrisPos: {e}")
            default_eye_data = {
                'lh': "UNREL_DATA",
                'lv': "UNREL_DATA",
                'lhd': "UNREL_DATA",
                'lvd': "UNREL_DATA",
                'attention':"UNREL_DATA"
            }
            return default_eye_data, default_eye_data
        
    def _normalize_position(self, position: str) -> float:
        """
        Convert categorical position to numerical representation
        
        Mapping based on cognitive tracking studies:
        Horizontal: Left (-1), Center (0), Right (1)
        Vertical: Down (-1), Center (0), Up (1)
        """
        position_map = {
            'left': -1.0,
            'center': 0.0,
            'right': 1.0,
            'down': -1.0,
            'up': 1.0
        }
        return position_map.get(position.lower(), 0.0)

    def update_eye_movement(self, 
                             horizontal_position: str, 
                             vertical_position: str) -> Dict[str, bool]:
        """
        Analyze eye movement for potential inattention markers
        
        Research Insights:
        - Prolonged deviation from central gaze indicates reduced attention
        - Rapid, erratic movements suggest cognitive load or distraction
        """
        h_pos = self._normalize_position(horizontal_position)
        v_pos = self._normalize_position(vertical_position)
        
        # Update movement histories
        self.horizontal_history.append(h_pos)
        self.vertical_history.append(v_pos)
        
        # Trim histories to maintain time window
        self.horizontal_history = self.horizontal_history[-self.time_window:]
        self.vertical_history = self.vertical_history[-self.time_window:]
        
        # Detect inattention markers
        horizontal_inattention = self._detect_deviation(
            self.horizontal_history, 
            self.horizontal_threshold
        )
        
        vertical_inattention = self._detect_deviation(
            self.vertical_history, 
            self.vertical_threshold
        )
        
        return {
            'horizontal_inattention': horizontal_inattention,
            'vertical_inattention': vertical_inattention,
            'overall_inattention': horizontal_inattention or vertical_inattention
        }
    

    def _detect_deviation(self, 
                          movement_history: List[float], 
                          threshold: float) -> bool:
        """
        Advanced deviation detection with multiple statistical checks
        
        Cognitive Research Indicators:
        1. Mean deviation from center
        2. Variance of movements
        3. Sustained off-center positioning
        """
        if len(movement_history) < self.time_window:
            return False
        
        # Calculate mean deviation
        mean_deviation = np.mean(np.abs(movement_history))
        movement_variance = np.var(movement_history)
        
        # Inattention criteria
        return (
            mean_deviation > threshold or 
            movement_variance > (threshold * 0.5)
        )



