import numpy as np
import time 
import cv2
from timerClock import clockTimer

UPPER_LIP = [13]
LOWER_LIP = [14]
LEFT_MOUTH_CORNER = [61]
RIGHT_MOUTH_CORNER = [291]

# Thresholds
YAWN_RATIO_UPPER_THRESHOLD = 0.6  # Upper limit for detecting a yawn
YAWN_RATIO_LOWER_THRESHOLD = 0.4  # Lower limit to reset the yawning state
ALERT_INTERVAL = 10  # Time interval in seconds
YAWN_TIMEFRAME = 20 #600



class YawnDetection:

    def __init__(self):
        self.yawn_counter = 0
        self.start_time = time.time()
        self.YAWNING_STATUS =  ['YAWNING',"NOT_YAWNING"]
        self.yawnign = self.YAWNING_STATUS[1] 
        self.ANOMALIES = ['UNREL_YAWN_DATA','LMK_AB']
        self.ANOMALY = self.ANOMALIES[1]
        self.historyQueue = [] # past history queue 
        self.clock = clockTimer()


    
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

                # print("History QUEUE ",self.historyQueue)

                

                cv2.putText(image, f"Yawn Ratio: {yawn_ratio:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(image, f"Yawn Count: {self.yawn_counter}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                try:
                    yawnCountTF,yawnLabel,timePeriodRun = self.getYawnsInTimeFrame(self.historyQueue,YAWN_TIMEFRAME)
                    cv2.putText(image, f"Yawns in TP: {yawnCountTF}", (10, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(image, f"Yawn Label: {yawnLabel}", (10, 370), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                except Exception as e: 
                    print("ERROR OCCURED IN getYAWNTF",e)
                    pass

                yawn_analysis = { 
                    "yawnCount":self.yawn_counter,
                    "yawnCountTF":yawnCountTF,
                    "yawnLabel":yawnLabel,
                    'timePeriodRun':timePeriodRun
                }

        else:
            return self.ANOMALY , self.ANOMALY,{}

        elapsed_time = time.time() - self.start_time
        if elapsed_time >= ALERT_INTERVAL :
            self.start_time = time.time()
            #logging to history Queue before setting yawn count to 0
            
            if(self.yawn_counter != 0 and self.yawn_counter >0 ):
                log = {
                "status":"YAWNED",
                "timeStamp":time.time() ,
                "count":self.yawn_counter
                }   
                self.historyQueue.append(log)
            
            
                
            #clearing History from yawn history log

            if(len(self.historyQueue)> 100):
                self.historyQueue.pop(0)
            
            self.yawn_counter = 0

        return image,self.yawning,yawn_analysis
    
    #calculates successive yawning count in 10 (set to 2 min in dev mode) min duration for frequent yawning detection 
    def getYawnsInTimeFrame(self,yawn_log : list,timePeriod: int ):
        size = len(yawn_log)
        curr_time = time.time()
        yawnCountTF = 0
        window_timeframe = 0

        #requires atleast 2 events 
        if(size>0):
            for i in range(size-1,-1,-1):
                yawnItem = yawn_log[i]['timeStamp']
                event_timeframe = self.clock.getTimerCount(yawnItem)
                
               
                if(event_timeframe <= timePeriod and event_timeframe > 0):
                    # print("event time frame",event_timeframe)
                    yawnCountTF += yawn_log[i]['count']
                
            window_timeframe = self.clock.getTimerCount(curr_time)
            # print("window time frame",window_timeframe)
            if(window_timeframe > timePeriod):
                self.clock.resetTimer()
                yawnCountTF = 0
                
            
        yawnLabel = self.getYawnClassfication(yawnCountTF)
        
        return yawnCountTF,yawnLabel, (window_timeframe == timePeriod )

                
        

    def getYawnClassfication(self,yawnCountTF : int):
        yawnStatus_label = "NORMAL_YAWNING" 
        
        if(yawnCountTF>=0 and yawnCountTF <= 4):
            yawnStatus_label = "NORMAL_YAWNING"
        elif(yawnCountTF>4 and yawnCountTF <= 8):
            yawnStatus_label = "MODERATE_YAWNING"
        elif(yawnCountTF>8 ):
            yawnStatus_label = "SEVERE_YAWNING"
        
        return yawnStatus_label


        



        
        

        
