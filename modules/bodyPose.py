import cv2
import numpy
import pandas as pd

class BodyPose:
    def __init__(self):
        self.pitch_array = []
        self.yaw_array = []
        self.self.FACE_STATES_PITCH = ['LOOKING_UP','FACE_UP','LOOKING_DOWN','FACE_DOWN']
        self.FACE_STATES_YAW = ['LOOKING_LEFT ','FACE_LEFT','LOOKING_RIGHT','FACE_RIGHT']
        self.COMBINED_STATES = ['TOP_LEFT',"TOP_RIGHT","BOTTOM_LEFT","BOTTOM_RIGHT"]
        self.CURRENT_STATE = "NO_STATE"
        self.CURRENT_COMBINED_STATE = "N0_STATE"

    def getHeadTiltStatus(self,face_landmarks,image):

        #getting image info
        img_h, img_w,img_channel = image.shape
        if face_ladmarks.multi_face_landmarks:
       
            for landmarks in face_ladmarks.multi_face_landmarks:
                face_2dCords = []
                face_3dCords = []
                
                for index,lnd in enumerate(landmarks.landmark):
                    # 1,33,263,61,241,144 : previous 
                    # 1,152,263,33,61,291
                    if  index == 1 or  index == 33 or  index == 263 or  index == 61 or  index == 291 or  index == 152:
                        if  index == 1:
                            Nose_2dCords = (int(lnd.x * img_w), int(lnd.y * img_h))
                            Nose_3dCords = (lnd.x * img_w, lnd.y * img_h,lnd.z * 3000)
                        
                        x,y = int(lnd.x * img_w), int(lnd.y * img_h)
                        face_2dCords.append([x,y])
                        face_3dCords.append([x,y,lnd.z])
        else:
            return image         



    def getHeadPos(self,pitch=0,yaw=0):
        if(pitch >=  13.5 and pitch < 19):
            self.CURRENT_STATE = self.FACE_STATES_PITCH[0]
        elif(pitch >= 19):
            self.CURRENT_STATE = self.FACE_STATES_PITCH[1] 
        elif(pitch <= -4 and pitch > -8 ):
            self.CURRENT_STATE = self.FACE_STATES_PITCH[2]
        elif(pitch < -8):
            self.CURRENT_STATE = self.FACE_STATES_PITCH[3]

   
        elif(yaw <= -7 and yaw > -15):
            self.CURRENT_STATE = self.FACE_STATES_YAW[2]
        elif(yaw < -15):
            self.CURRENT_STATE = self.FACE_STATES_YAW[3]
        elif(yaw >= 10 and yaw < 14):
            self.CURRENT_STATE = self.FACE_STATES_YAW[0]
        elif(yaw > 14):
            self.CURRENT_STATE = self.FACE_STATES_YAW[1]

            
        # combined state

        if(pitch >= 18.5 and yaw >= 10):
            self.CURRENT_COMBINED_STATE = self.COMBINED_STATES[0]
        elif(pitch >= 18.5 and yaw < -12):
            self.CURRENT_COMBINED_STATE = self.COMBINED_STATES[1]
        elif(pitch<-5 and yaw >= 8):
            self.CURRENT_COMBINED_STATE = self.COMBINED_STATES[2]
        elif(pitch<-6 and yaw <= -10):
            self.CURRENT_COMBINED_STATE = self.COMBINED_STATES[3]

        return self.CURRENT_STATE,self.CURRENT_COMBINED_STATE


    def calculateMovingAvarage(self,pitch:float , yaw:float ) -> tuple: 

        self.pitch_array.append(pitch)
        self.yaw_array.append(yaw)
       
        window_size = 6

        if(len(pitch_array)>window_size):
            pitch_array.pop(0)

        if(len(yaw_array)>window_size):
            yaw_array.pop(0)

        pitch_series = pd.Series(pitch_array)  
        yaw_series = pd.Series(yaw_array)  
        
        pitch_SMA = pitch_series.rolling(window_size).mean().iloc[-1] if len(pitch_array)>=window_size else 0
        yaw_SMA = yaw_series.rolling(window_size).mean().iloc[-1] if len(yaw_array)>=window_size else 0
            
        # print(f"Rolling Mean - pitch: {pitch_SMA}, yaw: {yaw_SMA}")
        return pitch_SMA,yaw_SMA