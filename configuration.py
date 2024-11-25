# import sys
# print(sys.path)

from components.eyeaspectRatio import EyeAspectRatio
from components.HeadPose import HeadPose
from components.YawnStatus import YawnDetection
from components.faceMesh import GetFaceMesh
from components.eyeballTrack import Eyeball
from components.projectUtils import UtlilitesFunction
import cv2,time  

capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
meshDraw = GetFaceMesh(refine_landmarks=True)
headpose = HeadPose()
eyeaspectratio = EyeAspectRatio()
yawnstatus = YawnDetection()
eyeballtrack = Eyeball()

def getVideoFeed():
    while True:
        isframe,frame = capture.read()

        if isframe:

            #getting facial landmarks data 
            frame,faces,facial_landmarks=meshDraw.findFaceMesh(frame,draw=True)

            #processing facial landmarks for different attributes 
            if facial_landmarks:
                #getting Head Tilt Status
                frame,currentState,combinedstate = headpose.getHeadTiltStatus(facial_landmarks,frame)

                #getting Eye Aspect Ratio
                meanEAR, right_EAR, left_EAR , eye_STATUS = eyeaspectratio.getEARs(faces,frame)

                #getting Yawn Status 
                _,yawnText = yawnstatus.getYawnStatusText(facial_landmarks,frame)#

                #getting eyeball tracking 
                left_eye,right_eye = eyeballtrack.getIrisPos(facial_landmarks,frame)   

                cv2.putText(frame, f"currentState {currentState}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"mean EAR {meanEAR}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f" Yawn Text : {yawnText}", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                # cv2.putText(image, f"Yawn Status: {self.yawnign}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                cv2.imshow("window",frame)

            else:
                cv2.imshow("window",frame)
                pass


        else:
            pass        
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyWindow()

#calling function    
getVideoFeed()