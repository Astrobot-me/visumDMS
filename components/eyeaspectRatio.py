# import sys
# sys.path.append(r'C:\Users\adity\OneDrive\Documents\drivermonitor\UmbrelaCorporation\modules\projectUtils.py')


from .projectUtils import UtlilitesFunction
import cv2


class EyeAspectRatio:

    def __init__(self):
        self.p1_RIGHT,self.p2_RIGHT,self.p3_RIGHT,self.p4_RIGHT,self.p5_RIGHT,self.p6_RIGHT = [33,133,144,160,153,158]
        self.p1_LEFT,self.p2_LEFT,self.p3_LEFT,self.p4_LEFT,self.p5_LEFT,self.p6_LEFT = [263,362,373,387,380,385]
        self.N1,self.N2 = [219,439]
        self.ear = [0.262,0.256,0.255,0.254,0.262]
        self.EAR_THRESHOLD = 0.250
        self.ANOMALIES = ['UNREL_EAR','LMK_AB']
        self.ANOMALY = self.ANOMALIES[0]
        self.utility = UtlilitesFunction()


    def getEARs(self,faces,image):
        if faces:
            face = faces[0]
            # print(face)
            for id in self.p1_RIGHT, self.p2_RIGHT , self.p3_RIGHT , self.p4_RIGHT , self.p5_RIGHT , self.p6_RIGHT:
                x,y = face[id]
                cv2.circle(image,center=(x,y),radius=2,color=(255,255,0),thickness=cv2.FILLED)
            
            for id in self.p1_LEFT,self.p2_LEFT,self.p3_LEFT,self.p4_LEFT,self.p5_LEFT,self.p6_LEFT:
                x,y = face[id]
                cv2.circle(image,center=(x,y),radius=2,color=(255,255,0),thickness=cv2.FILLED)
            
            # Right EyePoint Distance Calculation
            RIGHT_length1,info,image = self.utility.findDistance(face[self.p5_RIGHT],face[self.p6_RIGHT],image)
            RIGHT_length2,info,image = self.utility.findDistance(face[self.p3_RIGHT],face[self.p4_RIGHT],image)
            RIGHT_length3,info,image = self.utility.findDistance(face[self.p2_RIGHT],face[self.p1_RIGHT],image)

            # Left EyePoint Distance Calculation
            LEFT_length1,info,image = self.utility.findDistance(face[self.p5_LEFT],face[self.p6_LEFT],image)
            LEFT_length2,info,image = self.utility.findDistance(face[self.p3_LEFT],face[self.p4_LEFT],image)
            LEFT_length3,info,image = self.utility.findDistance(face[self.p2_LEFT],face[self.p1_LEFT],image)

            #Calculating Ear Aspect Ratio 
            EAR_ASPECT_RATIO_RIGHT = ((RIGHT_length2+RIGHT_length1)/2)/(RIGHT_length3)
            # print(f"Right Eye EAR: {EAR_ASPECT_RATIO_RIGHT}")

            #Calculating Ear Aspect Ratio 
            EAR_ASPECT_RATIO_LEFT = ((LEFT_length2+LEFT_length1)/2)/(LEFT_length3)
            # print(f"Left Eye EAR: {EAR_ASPECT_RATIO_LEFT}")

            AVERAGE_EAR = (EAR_ASPECT_RATIO_LEFT+EAR_ASPECT_RATIO_RIGHT)/2
            

            self.ear.append(AVERAGE_EAR)

            if(len(self.ear)>5):
                self.ear.pop(0)

            # print(self.ear)
            newEAR = sum(self.ear)/len(self.ear)

            if newEAR < self.EAR_THRESHOLD:
                # BLINK_COUNT = BLINK_COUNT + 1
                OBJECT_STATUS = "EYE_ABSENT"
                # print(f"STATUS: {OBJECT_STATUS}")
            else:
                OBJECT_STATUS = "EYE_PRESENT"
                # print(f"STATUS: {OBJECT_STATUS}")

            return newEAR,EAR_ASPECT_RATIO_RIGHT,EAR_ASPECT_RATIO_LEFT,OBJECT_STATUS
        else: 
            self.ANOMALY = self.ANOMALIES[1]
            return -1,-1, -1 , self.ANOMALY

