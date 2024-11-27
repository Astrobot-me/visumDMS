import cv2
import time
import asyncio
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

# Initialize objects
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
meshDraw = GetFaceMesh(refine_landmarks=True)
headpose = HeadPose()
eyeaspectratio = EyeAspectRatio()
yawnstatus = YawnDetection()
eyeballtrack = Eyeball()
faceexpression = FaceExpression()

def getVideoFeed():
    global currentState, combinedstate  # Declare as global

    while True:
        isframe, frame = capture.read()

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

            else:
                # No facial landmarks detected
                cv2.putText(frame, "Face Not Detected", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Show the frame
            cv2.imshow("window", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

# Calling the function
getVideoFeed()
