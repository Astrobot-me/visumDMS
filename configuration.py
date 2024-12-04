import cv2
import time
from threading import Thread, Event, Lock
from components.eyeaspectRatio import EyeAspectRatio
from components.HeadPose import HeadPose
from components.YawnStatus import YawnDetection
from components.faceMesh import GetFaceMesh
from components.eyeballTrack import Eyeball
from components.projectUtils import UtlilitesFunction
from components.faceExpression import FaceExpression
from process import processData,processPassiveData
from timerClock import clockTimer

# Initialize global variables
currentHeadState = "NONE"
combinedstate = "Not Detecting"
analysis_dict = None
terminate = False
frame = None
eye_STATUS = "NONE"
LABEL = "NONE"
count = 0
yawnAnalysisLog = {}
left_eye = {}
right_eye = {}
dataDict = {'data': False}
suggested_message = "NONE"

# Thread synchronization and locks
event = Event()
frame_lock = Lock()
analysis_dict_lock = Lock()

# Initialize objects
capture = cv2.VideoCapture(0)
meshDraw = GetFaceMesh(refine_landmarks=True)
headpose = HeadPose()
eyeaspectratio = EyeAspectRatio()
yawnstatus = YawnDetection()
eyeballtrack = Eyeball()
faceexpression = FaceExpression()


def getVideoFeed():
    global terminate, frame, eye_STATUS, dataDict, LABEL, suggested_message

    while not terminate:
        isframe, temp_frame = capture.read()
        if not isframe or temp_frame is None:
            print("Frame capture failed.")
            continue

        with frame_lock:
            frame = temp_frame

        event.set()  # Notify other threads

        try:
            # Getting facial landmarks
            temp_frame, faces, facial_landmarks = meshDraw.findFaceMesh(temp_frame, draw=True)

            if facial_landmarks.multi_face_landmarks:
                # Head Tilt Status
                _, currentHeadState, combinedstate = headpose.getHeadTiltStatus(facial_landmarks, temp_frame)

                # Eye Aspect Ratio
                meanEAR, right_EAR, left_EAR, eye_STATUS = eyeaspectratio.getEARs(faces, temp_frame)

                # Yawn Status
                _, yawnText, yawnAnalysisLog = yawnstatus.getYawnStatusText(facial_landmarks, temp_frame)

                # Eyeball Tracking
                left_eye, right_eye = eyeballtrack.getIrisPos(facial_landmarks, temp_frame)

                # Update data dictionary
                dataDict.update({
                    'data': True,
                    'eye_STATUS': eye_STATUS,
                    'currentHeadState': currentHeadState,
                    'yawnAnalysisLog': yawnAnalysisLog,
                    'left_eye': left_eye,
                    'right_eye': right_eye,
                })

                # Display data on the frame
                cv2.putText(temp_frame, f"Eye Attention L/R: {left_eye['attention']['overall_inattention']} "
                                        f"{right_eye['attention']['overall_inattention']}", (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(temp_frame, f"Current Head State: {currentHeadState}", (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(temp_frame, f"Mean EAR: {meanEAR}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(temp_frame, f"Yawn Text: {yawnText}", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                if analysis_dict:
                    with analysis_dict_lock:
                        cv2.putText(temp_frame, f"Recognized Emotion: {analysis_dict.get('dominantemotion', 'NONE')}", 
                                    (10, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                if LABEL != "NONE":
                    cv2.putText(temp_frame, f"LABEL: {LABEL}", (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    cv2.putText(temp_frame, f"COUNT: {count}", (10, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    cv2.putText(temp_frame, f"EYE: {eye_STATUS}", (10, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    cv2.putText(temp_frame, f"Message: {suggested_message}", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (255, 0, 0), 2)
            else:
                # No facial landmarks detected
                cv2.putText(temp_frame, "Face Not Detected", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                dataDict['data'] = False

            # Show the frame
            cv2.imshow("Driver Monitoring System", temp_frame)

        except Exception as e:
            print(f"Error during video feed processing: {e}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            terminate = True
            break

    capture.release()
    cv2.destroyAllWindows()


def getRealEmoText():
    global terminate, frame, analysis_dict

    while not terminate:
        event.wait()
        with frame_lock:
            temp_frame = frame.copy() if frame is not None else None

        if temp_frame is not None:
            try:
                with analysis_dict_lock:
                    analysis_dict = faceexpression.getFaceExpression(temp_frame)
            except Exception as e:
                print(f"Error in face expression detection: {e}")

        time.sleep(2)


def runStateProcessCounter():
    global LABEL, count, suggested_message, dataDict

    clocktimer = clockTimer()  # Timer object
    clocktimer.resetTimer()

    while not terminate:
        time.sleep(1)
        try:
            LABEL, count = processData(dataDict, clocktimer)
            print(" Yawn Dict :", dataDict.get('yawnAnalysisLog'))
            suggested_message = processPassiveData(dataDict.get('yawnAnalysisLog'),"NONE","NONE")
            print("Suggested Message",suggested_message)
        except Exception as e:
            print(f"Error in state process counter: {e}")


# if __name__ == "__main__":
#     # Start threads
#     video_thread = Thread(target=getVideoFeed, daemon=True)
#     emotion_thread = Thread(target=getRealEmoText, daemon=True)
#     state_thread = Thread(target=runStateProcessCounter, daemon=True)

#     video_thread.start()
#     emotion_thread.start() 
#     state_thread.start()

#     video_thread.join()
#     emotion_thread.join()
#     state_thread.join()

#     print("Program terminated.")
