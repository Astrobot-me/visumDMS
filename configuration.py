import cv2
import time
from threading import Thread, Event, Lock
from components.eyeaspectRatio import EyeAspectRatio
from components.HeadPose import HeadPose
from components.YawnStatus import YawnDetection
from components.faceMesh import GetFaceMesh
from components.eyeballTrack import Eyeball
from components.projectUtils import UtlilitesFunction
import locationServer
from sendSms import sms_notifier
# from components.faceExpression import FaceExpression
from process import processData,processPassiveData
from timerClock import clockTimer
from audioAlert import playAlarm
from dbCon import firestore_instance
import CONSTANTS
import datetime,serial
import numpy as np



# Initialize global variables
currentHeadState = "NONE"
combinedstate = "Not Detecting"
analysis_dict = None
terminate = False
frame = None
state_frame = None
eye_STATUS = "NONE"
LABEL = "NONE"
CON_STATUS = "NOT CON"
last_label = None
count = 0
yawnAnalysisLog = {}
left_eye = {}
right_eye = {}
dataDict = {'data': False}
suggested_message = "NONE"
Background = None
CONTACT = "+917004433613"

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
# faceexpression = FaceExpression()
util = UtlilitesFunction()
try:
    ser = serial.Serial('COM3', 9600)
    CON_STATUS = "CONNECTED"
except: 
    pass




def getVideoFeed():
    global terminate, frame,state_frame, eye_STATUS, dataDict, LABEL, suggested_message
    global Background

    print(f"[VIDEOFEED/T1] : Starting Videofeed")

    while not terminate:


        Background = cv2.imread("./resources/skeleton3.png")


        isframe, temp_frame = capture.read()
        temp_frame = util.rescaleFrame(temp_frame,0.9)
        if not isframe or temp_frame is None:
            print("Frame capture failed.")
            continue

        with frame_lock:
            frame = temp_frame
            state_frame = temp_frame.copy()

        event.set()
          # Notify other threads

        # print(Background.shape[0], Background.shape[1])
        # Background = util.rescaleFrame(Background,0.9)
        Background[100:100+temp_frame.shape[0], 580:580+temp_frame.shape[1]] = temp_frame

        try:
            # Getting facial landmarks
            temp_frame, faces, facial_landmarks = meshDraw.findFaceMesh(temp_frame, draw=False)
            state_frame = temp_frame.copy()

            if facial_landmarks.multi_face_landmarks:
                # Head Tilt Status
                _, currentHeadState, combinedstate = headpose.getHeadTiltStatus(facial_landmarks, temp_frame)

                # Eye Aspect Ratio
                meanEAR, right_EAR, left_EAR, eye_STATUS = eyeaspectratio.getEARs(faces, temp_frame)

                # Yawn Status
                _, yawnText, yawnAnalysisLog = yawnstatus.getYawnStatusText(facial_landmarks, temp_frame)

                # Eyeball Tracking
                left_eye, right_eye = eyeballtrack.getIrisPos(facial_landmarks, temp_frame)

                #base 64 image conversionn

                     

                # Update data dictionary
                dataDict.update({
                    'data': True,
                    'meanEAR':meanEAR,
                    'eye_STATUS': eye_STATUS,
                    'currentHeadState': currentHeadState,
                    'yawnAnalysisLog': yawnAnalysisLog,
                    'left_eye': left_eye,
                    'right_eye': right_eye,
                })

                # Display data on the frame
                # cv2.putText(temp_frame, f"Eye Attention L/R: {left_eye['attention']['overall_inattention']} "
                #                         f"{right_eye['attention']['overall_inattention']}", (10, 90),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                # cv2.putText(temp_frame, f"Current Head State: {currentHeadState}", (10, 120),
                
                
                # Head State
                #cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(Background,currentHeadState,(65,537),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1.5,color=CONSTANTS.RED_COLOR,thickness=3,lineType=cv2.LINE_8) 

                # MEAR EAR
                # cv2.putText(temp_frame, f"Mean EAR: {meanEAR}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(Background,str(round(meanEAR,3)),(65,290),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1.8,color=CONSTANTS.BLACK_COLOR,thickness=3,lineType=cv2.LINE_8) 


                #Yawn Text
                #cv2.putText(temp_frame, f"Yawn Text: {yawnText}", (10, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                # print("--YAL-- : ", yawnAnalysisLog)
                if Background is not None:
                    cv2.putText(Background,str(yawnText),(70,674),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.85,color=CONSTANTS.BLACK_COLOR,thickness=2,lineType=cv2.LINE_8)
                    cv2.putText(Background,str(yawnAnalysisLog.get("yawnCount","N/A")),(350,674),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1.0,color=CONSTANTS.BLACK_COLOR,thickness=2,lineType=cv2.LINE_8)

                    cv2.putText(Background,yawnAnalysisLog.get('yawnLabel',"N/A"),(70,754),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.85,color=CONSTANTS.BLACK_COLOR,thickness=2,lineType=cv2.LINE_8)
                    cv2.putText(Background,str(yawnAnalysisLog.get('yawnCountTF',"N/A")),(350,754),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1.0,color=CONSTANTS.BLACK_COLOR,thickness=2,lineType=cv2.LINE_8)
                else:
                    print("Background image is None, cannot place text.")


                if analysis_dict:
                    with analysis_dict_lock:
                        cv2.putText(temp_frame, f"Recognized Emotion: {analysis_dict.get('dominantemotion', 'NONE')}", 
                                    (10, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                
            else:
                #notdone
                # No facial landmarks detected
                cv2.putText(temp_frame, "Face Not Detected", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                dataDict['data'] = False
            

            if LABEL != "NONE":
                    # cv2.putText(temp_frame, f"LABEL: {LABEL}", (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    cv2.putText(Background,LABEL,(1294,163),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1.2,color=CONSTANTS.LABEL_COLOR,thickness=3,lineType=cv2.LINE_8)

                    # cv2.putText(temp_frame, f"COUNT: {count}", (10, 280), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    cv2.putText(Background,f"{str(count)} Secs",(1294,288),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1.8,color=CONSTANTS.BLUE_COLOR,thickness=3,lineType=cv2.LINE_8)


                    #Utilities 
                   

                    #Eye State
                    #cv2.putText(temp_frame, f"EYE: {eye_STATUS}", (49, 336), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                    cv2.putText(Background,f"{eye_STATUS}",(69,420),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1.8,color=CONSTANTS.BLUE_COLOR,thickness=3,lineType=cv2.LINE_8)



                    # cv2.putText(Background,meanEAR,(210,49),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1.8,color=CONSTANTS.BLACK_COLOR,thickness=3,lineType=cv2.LINE_8)
                    # cv2.putText(temp_frame, f"Message: {suggested_message}", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    #             (255, 0, 0), 2)

            # Show the frame
            cv2.imshow("Driver Monitoring System", Background)

        except Exception as e:
            print(f"Error during video feed processing: {e}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            terminate = True
            break

    capture.release()
    cv2.destroyAllWindows()





def logIntoDb(): 
    global LABEL,last_label ,eye_STATUS,Background,dataDict
    global frame,state_frame

    
    print("[LOCATION] : ", locationServer.location)
    while not terminate:
        
        

        if last_label == None : 
            last_label  = LABEL 
        elif LABEL != "None" and LABEL != last_label: 
            last_label = LABEL
            
           
            
            try:
                if state_frame is not None and isinstance(state_frame, np.ndarray):
                    base64Text = util.convertToBase64(state_frame)
                else:
                    print("[logIntoDb] Warning: state_frame is None or invalid. Using placeholder.")
                    base64img = cv2.imread(r"resources/placeholder.png")
                    base64Text = util.convertToBase64(base64img)
            except Exception as e:
                print(f"[logIntoDb] Error during frame to base64 conversion: {e}")
                return

            # base64Text = util.frame_to_base64(state_frame)  
     
        
            # inserting into database

            yawn_phase_count = dataDict.get('yawnAnalysisLog', {}).get('yawnCountTF', "N/A")
            yawn_phase_state = dataDict.get('yawnAnalysisLog', {}).get('yawnLabel', "N/A")
            reported_ear = dataDict.get('meanEAR',0.0)
            lat = float(locationServer.location['latitude'])
            long = float(locationServer.location['longitude'])
            head_state = dataDict.get('currentHeadState',"NO_STATE")

            firestore_instance.insert_into_db(
                head_state=head_state,
                eye_state=eye_STATUS, 
                hazard_status=LABEL, 
                yawn_phase_count=yawn_phase_count,
                yawn_phase_state=yawn_phase_state, 
                reported_ear=float(reported_ear), 
                img_frame=base64Text,
                sos_state=False,
                current_vehicle_status="STOPPED",
                alcohol_quantity="20%", 
                driver_reported_image="",
                lat=locationServer.location['latitude'], 
                long=locationServer.location['longitude'], 
                location_text=str(locationServer.location['address']),
                maps_link=f"https://www.google.com/maps?q={'28.974033'},{'77.640352'}"
            )

            logtime = datetime.datetime.now()
            message = f"[DATABASE] Logged Into Database : {logtime.strftime(' %d/%m/%Y, %H:%M:%S ')}"
            print(message)
            cv2.putText(Background,str(message), (544,750),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=1.5,color=(255,255,255),thickness=2,lineType=cv2.LINE_4)


            



# def getRealEmoText():
#     global terminate, frame, analysis_dict

#     # PASSING TO skip the facial emotion module
#     pass 
#     while not terminate:
#         event.wait()
#         with frame_lock:
#             temp_frame = frame.copy() if frame is not None else None

#         if temp_frame is not None:
#             try:
#                 with analysis_dict_lock:
#                     analysis_dict = faceexpression.getFaceExpression(temp_frame)
#             except Exception as e:
#                 print(f"Error in face expression detection: {e}")

#         time.sleep(2)


def runStateProcessCounter():
    global LABEL, last_label,count, suggested_message, dataDict,Background
    global CONTACT


    print(f"[PROCESS/T3] : Starting Process Counter")
    clocktimer = clockTimer()  # Timer object
    clocktimer.resetTimer()

    while not terminate:
        time.sleep(1)
        try:
            LABEL, count = processData(dataDict, clocktimer,20,True)
            state = 1
            hazard_alert_sent = False

            # playing alarm
            playAlarm(LABEL)       


            try: 
                if LABEL == "SAFE": 
                    state = 1    
                    hazard_alert_sent = False
                    try: 
                        ser.write(str(state).encode())
                    except:
                        pass

                elif LABEL == "CAUTION": 
                    state = 2
                    try: 
                        ser.write(str(state).encode())
                    except:
                        pass

                    # Implement Twilio 
                    if not hazard_alert_sent:
                        loc_text,_link = sms_notifier.get_location_info()


                        loc_text = "Delhi Roorkee Bypass Road, Meerut"
                        _link = "https://maps.google.com/?q=28.9845,77.7064"

                        # sms_notifier.send_sms(f"🚨 Hazard Detected! Driver unresponsive\n location : {loc_text} \nLive Link : {_link}", CONTACT)
                        logtime = datetime.datetime.now()
                        message = f"[SMS API] Logged Into Database : {logtime.strftime(' %d/%m/%Y, %H:%M:%S ')}"
                        cv2.putText(Background,str(message), (544,790),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=1.5,color=(255,255,255),thickness=2,lineType=cv2.LINE_4)
                elif LABEL == "HAZARD":
                    state = 3 
                    try: 
                        ser.write(str(state).encode())
                    except:
                        pass
                    
                else : 
                    try: 
                        ser.flushInput()
                        if ser.in_waiting > 0:
                            line = ser.readline().decode('utf-8').strip()
                            if line == '-1':
                                LABEL = "HAZARD"; 
                                state = 3
                                ser.write(str(state).encode())
                    except:
                        pass
 
                 

            except Exception as e: 
                print(f"Exception Occured in Sending state f{e}")


            suggested_message = processPassiveData(dataDict.get('yawnAnalysisLog'),"NONE","NONE",True)

            if CON_STATUS == "CONNECTED" and Background is not None:
                cv2.putText(Background,f"Status {state} Sent Successfully", (504,650),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=1.5,color=(255,255,255),thickness=2,lineType=cv2.LINE_4) # STA_LOG2
            else:
                cv2.putText(Background,f"Please Conn the Controller", (534,670),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=1.9,color=(255,255,255),thickness=2,lineType=cv2.LINE_4)

            cv2.putText(Background,suggested_message, (534,750),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=1.5,color=(255,255,255),thickness=2,lineType=cv2.LINE_4)

 
            
            # print("Suggested Message",suggested_message)
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
