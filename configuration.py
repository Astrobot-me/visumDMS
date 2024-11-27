import cv2
import time
from threading import Thread,Event
from components.eyeaspectRatio import EyeAspectRatio
from components.HeadPose import HeadPose
from components.YawnStatus import YawnDetection
from components.faceMesh import GetFaceMesh
from components.eyeballTrack import Eyeball
from components.projectUtils import UtlilitesFunction
from components.faceExpression import FaceExpression

# Initialize global variables
currentState = "Not Detecting"
combinedstate = "Not Detecting"
analysis_dict = None
terminate = False
frame = None

# Initialize objects
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
meshDraw = GetFaceMesh(refine_landmarks=True)
headpose = HeadPose()
eyeaspectratio = EyeAspectRatio()
yawnstatus = YawnDetection()
eyeballtrack = Eyeball()
faceexpression = FaceExpression()
event = Event()

def getVideoFeed():
    global currentState, combinedstate,analysis_dict  # Declare as global
    global terminate
    global frame
    
    while True:
        isframe, frame = capture.read()
        # rgb_frame = frame
        event.set()
        print("---- WATING FOR EMOTION RECOGNITION ----")   

        if analysis_dict == None: 
            print("GET VIDEOFEED THREAD ON WAIT ")
            event.wait()

        print("---- EMOTION RECOGNISED ----")   
        
        if isframe:
            # Getting facial landmarks data
            frame, faces, facial_landmarks = meshDraw.findFaceMesh(frame, draw=True)

            # Processing facial landmarks for different attributes
            if facial_landmarks:
                try:
                    # Getting Head Tilt Status
                    _, currentState, combinedstate = headpose.getHeadTiltStatus(facial_landmarks, frame)

                except Exception as e:
                    currentState = "Not Detecting"
                    combinedstate = "Not Detecting"
                    print(f"Head pose detection error: {e}")

                try:
                    # Getting Eye Aspect Ratio
                    meanEAR, right_EAR, left_EAR, eye_STATUS = eyeaspectratio.getEARs(faces, frame)
                    print(eye_STATUS)
                except Exception as e:
                    meanEAR, eye_STATUS = "Not Detecting", "Not Detecting"
                    print(f"Eye detection error: {e}")

                try:
                    # Getting Yawn Status
                    _, yawnText = yawnstatus.getYawnStatusText(facial_landmarks, frame)
                except Exception as e:
                    yawnText = "Not Detecting"
                    print(f"Yawn detection error: {e}")

                try:
                    # Getting eyeball tracking
                    left_eye, right_eye = eyeballtrack.getIrisPos(facial_landmarks, frame)
                except Exception as e:
                    left_eye, right_eye = "Not Detecting", "Not Detecting"
                    print(f"Eyeball tracking error: {e}")
 

                # Display information on the frame
                cv2.putText(frame, f"currentState: {currentState}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"mean EAR: {meanEAR}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Yawn Text: {yawnText}", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                if analysis_dict != None:
                    print("Emodict",analysis_dict)
                    cv2.putText(frame, f"Recog emotion: {analysis_dict['dominantemotion']}", (10, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    pass 

            else:
                # No facial landmarks detected
                cv2.putText(frame, "Face Not Detected", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Show the frame
            cv2.imshow("window", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            terminate = True
            break

    capture.release()
    cv2.destroyAllWindows()

# Calling the function
# getVideoFeed()


def getRealEmoText():
    global terminate,frame,analysis_dict
    
    print("---- WAITING FOR VIDEO FRAME ----")
    event.wait()
    # try:
    #     analysis_dict = faceexpression.getFaceExpression(rgb_frame)
    # except:
    #     pass
    analysis_dict = faceexpression.getFaceExpression(frame)
    print("---- VIDEO RESUMED && ANLYSIS DICT SET ----")
    event.set() 

    while True: 
        # try: 
        #     
        # except:
        #     pass
        analysis_dict = faceexpression.getFaceExpression(frame)
        if terminate:
            break 

        
