from modules import eyeaspectRatio
from modules import HeadPose
from modules import YawnStatus
from modules import faceMesh
from modules import eyeballTrack
from modules import utilities
import cv2,time  

capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
meshDraw = faceMesh.GetFaceMesh()
headpose = HeadPose.HeadPose()

def getVideoFeed():
    isframe,frame = capture.read()

    if isframe:

        #getting facial landmarks data 
        frame,faces,facial_landmarks=meshDraw.findFaceMesh(frame,draw=True)

        #getting Head Tilt Status
        if facial_landmarks:
            frame,currentState,combinedstate = headpose.getHeadTiltStatus(face_landmarks,frame)

    else:
        pass        
 

