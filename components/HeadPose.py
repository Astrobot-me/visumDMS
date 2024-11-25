import cv2
import numpy
import pandas as pd

class HeadPose:
    def __init__(self):
        self.pitch_array = []
        self.yaw_array = []
        self.FACE_STATES_PITCH = ['LOOKING_UP','FACE_UP','LOOKING_DOWN','FACE_DOWN']
        self.FACE_STATES_YAW = ['LOOKING_LEFT ','FACE_LEFT','LOOKING_RIGHT','FACE_RIGHT']
        self.COMBINED_STATES = ['TOP_LEFT',"TOP_RIGHT","BOTTOM_LEFT","BOTTOM_RIGHT"]
        self.CURRENT_STATE = "NO_STATE"
        self.CURRENT_COMBINED_STATE = "N0_STATE"
        self.window_size = 6
        
    def getHeadTiltStatus(self,face_landmarks,image):

        #getting image info
        img_h, img_w,img_channel = image.shape
        if face_landmarks.multi_face_landmarks:
       
            for landmarks in face_landmarks.multi_face_landmarks:
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


        face_2dCords = numpy.array(face_2dCords,dtype=numpy.float64)
        face_3dCords = numpy.array(face_3dCords,dtype=numpy.float64)


        focal_length = 1 * img_w
        cameraMatrix = numpy.array([[
            focal_length,0,img_h/2
        ],[
            0,focal_length,img_w/2
        ],[
            0,0,1
        ]],dtype=numpy.float64)

        distortionMatrix = numpy.zeros((4,1))
        isTranslate, rvec, tvec = cv2.solvePnP(face_3dCords,face_2dCords,cameraMatrix,distortionMatrix) 
        rotationMatrix, _ = cv2.Rodrigues(rvec)

        rotationAngles,mtxR,mtxQ,qx,qy,qz = cv2.RQDecomp3x3(rotationMatrix)
    
        pitch= rotationAngles[0]
        yaw = rotationAngles[1]
        roll = rotationAngles[2]

        # # Normalized Values of pitch,yaw & roll
        pitch = pitch * 360
        yaw = yaw * 360
        roll = roll * 360
    
        pitch,yaw = self.calculateMovingAvarage(pitch,yaw)

        currentstate,combinedstate = self.getHeadPos(pitch,yaw)

        # if(CurrentStateText1!=None):
        #     cv2.putText(image,CurrentStateText1, (200,30),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=2,color=(0,0,255),thickness=2)
        # if(CurrentStateText2 != None):
        #     cv2.putText(image,CurrentStateText2, (200,300),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=2,color=(0,0,255),thickness=2)


        print(f"Pitch :{pitch}, Yaw: {yaw}, Roll:{roll}")
        axis = numpy.float32([[10, 0, 0], [0, 10, 0], [0, 0, 10]])
        nose3d_realization,_ = cv2.projectPoints(axis,rvec,tvec,cameraMatrix,distortionMatrix)
    
        #dynamic Scaling of head pose line 
        base_scaling_factor = 10
        distance_from_camera = tvec[2][0]

        dynamic_scaling_factor = base_scaling_factor/max(1,distance_from_camera/1000)
        
        if nose3d_realization is not None:
            # nose_point = (int(landmarks[1].x * img_w), int(landmarks[1].y * img_h))
            
            x_axis = (int(nose3d_realization[0][0][0]), int(nose3d_realization[0][0][1]))
            y_axis = (int(nose3d_realization[1][0][0]), int(nose3d_realization[1][0][1]))
            z_axis = (int(nose3d_realization[2][0][0]), int(nose3d_realization[2][0][1]))


            # Ensure nose3d_realization has enough points before accessing them
            if len(nose3d_realization) >= 3:
                # Draw the X, Y, and Z axes
                cv2.line(image, Nose_2dCords,x_axis , (0, 0, 255), 3)  # X-axis (red)
                cv2.line(image, Nose_2dCords,y_axis , (0, 255, 0), 3)  # Y-axis (green)
                cv2.line(image, Nose_2dCords, z_axis, (255, 0, 0), 3)  # Z-axis (blue)


        
        # Add the text on the image
        cv2.putText(image, "x: " + str(numpy.round(pitch, 2)), (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(image, "y: " + str(numpy.round(yaw, 2)), (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(image, "z: " + str(numpy.round(roll, 2)), (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        return image, currentstate,combinedstate         



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
       
        

        if(len(self.pitch_array)>self.window_size):
            self.pitch_array.pop(0)

        if(len(self.yaw_array)>self.window_size):
            self.yaw_array.pop(0)

        pitch_series = pd.Series(self.pitch_array)  
        yaw_series = pd.Series(self.yaw_array)  
        
        pitch_SMA = pitch_series.rolling(self.window_size).mean().iloc[-1] if len(self.pitch_array)>=self.window_size else 0
        yaw_SMA = yaw_series.rolling(self.window_size).mean().iloc[-1] if len(self.yaw_array)>=self.window_size else 0
            
        # print(f"Rolling Mean - pitch: {pitch_SMA}, yaw: {yaw_SMA}")
        return pitch_SMA,yaw_SMA