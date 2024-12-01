import numpy as np
import time 
import cv2

UPPER_LIP = [13]
LOWER_LIP = [14]
LEFT_MOUTH_CORNER = [61]
RIGHT_MOUTH_CORNER = [291]

# Thresholds
YAWN_RATIO_UPPER_THRESHOLD = 0.6  # Upper limit for detecting a yawn
YAWN_RATIO_LOWER_THRESHOLD = 0.4  # Lower limit to reset the yawning state
ALERT_THRESHOLD = 3  # Number of yawns for an alert
ALERT_INTERVAL = 10  # Time interval in seconds
# ALERT_SOUND_DURATION = 15



class YawnDetection:

    def __init__(self):
        self.yawn_counter = 0
        self.start_time = time.time()
        self.YAWNING_STATUS =  ['YAWNING',"NOT_YAWNING"]
        self.yawnign = self.YAWNING_STATUS[1] 
        self.ANOMALIES = ['UNREL_YAWN_DATA','LMK_AB']
        self.ANOMALY = self.ANOMALIES[1]
        self.historyQueue = [] # past history queue 

    
    def getYawnStatusText(self,resultSetLandmark,image):
        height, width, _ = image.shape
        if resultSetLandmark.multi_face_landmarks:
            for face_landmarks in resultSetLandmark.multi_face_landmarks:
            # Extract the landmark coordinates
                landmarks = np.array([[lm.x * width, lm.y * height] for lm in face_landmarks.landmark])

                # Calculate mouth distances
                upper_lip = landmarks[UPPER_LIP[0]]
                lower_lip = landmarks[LOWER_LIP[0]]
                left_corner = landmarks[LEFT_MOUTH_CORNER[0]]
                right_corner = landmarks[RIGHT_MOUTH_CORNER[0]]

                vertical_distance = np.linalg.norm(upper_lip - lower_lip)
                horizontal_distance = np.linalg.norm(left_corner - right_corner) 

                yawn_ratio = vertical_distance / horizontal_distance

                if yawn_ratio > YAWN_RATIO_UPPER_THRESHOLD:
                    if not (self.yawning == self.YAWNING_STATUS[0]):
                        self.yawning = self.YAWNING_STATUS[0]
                        self.yawn_counter += 1
                elif yawn_ratio < YAWN_RATIO_LOWER_THRESHOLD:
                    self.yawning = self.YAWNING_STATUS[1]

                print("History QUEUE ",historyQueue)

                

                cv2.putText(image, f"Yawn Ratio: {yawn_ratio:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(image, f"Yawn Count: {self.yawn_counter}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(image, f"Yawn Status: {self.yawnign}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            return self.ANOMALY , self.ANOMALY,{}

        elapsed_time = time.time() - self.start_time
        if elapsed_time >= ALERT_INTERVAL :
            self.start_time = time.time()
            #logging to history Queue before setting yawn count to 0
            if (self.yawnign == 'YAWNING'):
                log = {
                    "status":yawn_status,
                    "timeStamp":time.time() ,
                    "count":self.yawn_counter
                }
                historyQueue.append(log)
            
            
                
            #clearing History from yawn history log

            if(len(self.historyQueue)> 20):
                self.historyQueue.pop(0)
            
            self.yawn_counter = 0

        return image,self.yawning,self.historyQueue
    
    #calculates successive yawning count in 10 min duration for frequent yawning detection 
    def getYawnsInTimeFrame(yawn_log: list):
        size = len(yawn_log)
        if(size>3):
            last_yawn = yawn_log[size-1]
            prev_last_yawn = yawn_log[size-2]
            antipenultimate_yawn = yawn_log[size-3]
            #finding last YAWNING Event

            last2_yawnDuration = float(last_yawn["timeStamp"] - prev_last_yawn["timeStamp"]) 
            penUltimate_yawnDuration = float(antipenultimate_yawn["timeStamp"] - last_yawn["timeStamp"]) 

    def getYawnClassfication():
        pass

        



        
        

        
