from timerClock import clockTimer
import time
from collections import deque
# clocktimer = clockTimer()


STATES = ["CAUTION","SAFE","HAZARD","DRIVER NOT FOUND","PRECAUTION"]
# count = 0
headpose_caution_states = ['LOOKING_DOWN','FACE_DOWN','FACE_DOWN','BOTTOM_LEFT','BOTTOM_RIGHT']
suggested_message_states = [
    "All fine and Driver is wide awake",
    "Your attention belongs to Road",
    'Eyes on the road! Stay alert to ensure your safety',
    'You seem a bit distracted. Refresh yourself before continuing',
    "Driver Look Tired , Please Consider taking Rest",
    " Look extremely Tired, it is Suggested to Take Rest",
    "You seems Sleepy , Park car and Take a nap"
]

critical_message_states = [
    'Plan your next rest stop. A short break can keep you safe.',
    'You Look Tired , Please Consider taking Rest',
    'You’re showing signs of tiredness. Drive Safetly',
    'Critical alert! You look too tired to drive safely. Stop immediately.',
    

]

hardware_info_states = [
    'You Have High Alcohol Content , Driving is Not permitted'
]


yawn_status_history = deque(maxlen=50)


def processData(dataDict: dict, counterOBJ,  vehicle_speed :int = 20,alcoholParam:bool=False ):

    message_state = STATES[1]


    #Toggling if we have consider the hardware info or not
    vehicle_speed = vehicleSpeedParamToggler(True,vehicle_speed)
    alcoholParam = alcoholParamToggler(False,alcoholParam)
    # print("Data dict--- ",dataDict)

    if dataDict['data']:
        
        eye_status = dataDict['eye_STATUS']
        head_pose = dataDict['currentHeadState']
        yawnAnalysisLog = dataDict['yawnAnalysisLog']
        left_eye = dataDict['left_eye']
        rigth_eye = dataDict['right_eye']



        if not alcoholParam:

            if eye_status == "EYE_PRESENT" and  head_pose not in headpose_caution_states:
                count = 0
                counterOBJ.resetTimer()
                message_state = STATES[1]
                # suggested_message = processPassiveData(yawnAnalysisLog,"NOnE","NONE")
                return message_state,count

            elif(eye_status == "EYE_ABSENT" ):
                count = counterOBJ.getTimerCount(time.time())

                if vehicle_speed > 5:
                    if count > 1 and count <= 4: 
                        message_state = STATES[0]
                    elif count > 4:
                        message_state = STATES[2]

                elif (vehicle_speed > 1 and vehicle_speed <= 5):
                    if count > 15 and count <= 25: 
                        message_state = STATES[0]
                    elif count > 25:
                        message_state = STATES[2]
                elif vehicle_speed == 0:
                    count = 0
               
                return message_state,count

            elif( eye_status == "EYE_ABSENT" and head_pose in headpose_caution_states ):
                count = counterOBJ.getTimerCount(time.time())


                if vehicle_speed > 5:
                    if count > 2 and count <= 6 : 
                        message_state = STATES[4]
                    elif count > 6 and count <= 10:
                        message_state = STATES[0]
                    elif count > 10:
                        message_state = STATES[2]

                elif (vehicle_speed > 1 and vehicle_speed <= 5):
                    if count > 10 and count <= 20 : 
                        message_state = STATES[4]
                    elif count > 30 and count <= 40:
                        message_state = STATES[0]
                    elif count > 40:
                        message_state = STATES[2]
                elif vehicle_speed == 0:
                    count = 0

                return message_state,count

            elif(head_pose in headpose_caution_states):
                count = counterOBJ.getTimerCount(time.time())

                
                if vehicle_speed > 5:
                    if count > 1 and count <= 8: 
                        message_state = STATES[0]
                    elif count > 8:
                        message_state = STATES[2]

                elif (vehicle_speed > 1 and vehicle_speed <= 5):
                    if count > 30 and count <= 60: 
                        message_state = STATES[0]
                    elif count > 60:
                        message_state = STATES[2]
                elif vehicle_speed == 0:
                    count = 0

                return message_state,count
        else:
            message_state = STATES[2]
            return message_state,-1
    else:
        count = counterOBJ.getTimerCount(time.time())

        if vehicle_speed > 5:
            if count > 2 and count <= 30: 
                message_state = STATES[3]
            elif count > 30:
                message_state = STATES[2]
        elif (vehicle_speed > 1 and vehicle_speed <= 5):
            if count > 60 : 
                message_state = STATES[2]
        elif vehicle_speed == 0:
                    count = 0
        
        
        return message_state,count
        
    # if( left_eye['lhd'] == "DOWN" and rigth_eye == 'DOWN' ):
    #     if(len(yawnAnalysis.keys())>0):
    #         count = counterOBJ.getTimerCount(time.time())

    #         if count > 1 and count <= 6 : 
    #             message_state = STATES[0]
    #         elif count > 6:
    #             message_state = STATES[2]

    #         return message_state,count



def processPassiveData(yawnAnalysis: dict , face_emotion:str , eye_tracking_data : str,alcoholParam:bool=False):
    # yawn_analysis = { 
    #                     "yawnCountTF":yawnCountTF,
    #                     "yawnLabel":yawnLabel,
    #                     'timePeriodRun':timePeriodRun
    #                 }

    global yawn_status_history

    suggestion_message = suggested_message_states[0]

    alcoholParam = alcoholParamToggler(False,alcoholParam)

    if alcoholParam : 
        suggestion_message = hardware_info_states[0]
        return suggestion_message

    # if(yawnAnalysis['yawnLabel'] == "SEVERE_YAWNING"):

    #     suggestion_message = suggested_message_states[2]
    #     return suggestion_message


    if(len(yawn_status_history) == 0 ):
        yawn_status_history.append({
            "count":yawnAnalysis['yawnCountTF'],
            "label":yawnAnalysis['yawnLabel'],
            "timeStamp":time.time()

        })
        print(" Yawn History Text: ",yawn_status_history)

    elif (len(yawn_status_history)>0 and yawnAnalysis['timePeriodRun']):

        print(" Yawn History Text: ",yawn_status_history)
        yawn_status_history.append({
            "count":yawnAnalysis['yawnCountTF'],
            "label":yawnAnalysis['yawnLabel'],
            "timeStamp":time.time()

        })
    

    # Step 3: Check history and determine state
    history_length = len(yawn_status_history)
        

    if history_length >= 3:
        # Logic for 3-element history
        last_three = list(yawn_status_history)[-3:]
        labels = [entry['label'] for entry in last_three]

       
        if labels == ["MODERATE_YAWNING", "MODERATE_YAWNING", "MODERATE_YAWNING"]:
            suggestion_message = suggested_message_states[4]
            return suggestion_message
        
        elif labels == ["SEVERE_YAWNING", "SEVERE_YAWNING", "SEVERE_YAWNING"]:
            suggestion_message = critical_message_states[3]
            return suggestion_message
        
        elif labels.count("MODERATE_YAWNING") >= 2 and labels.count("SEVERE_YAWNING") >= 1 :
            suggestion_message = critical_message_states[0]
            return suggestion_message
        
        elif labels.count("SEVERE_YAWNING") >= 2 and labels.count("MODERATE_YAWNING") >= 1 :
            suggestion_message = critical_message_states[2]
            return suggestion_message
       
        elif "SEVERE_YAWNING" in labels:
            suggestion_message = critical_message_states[1]
            return suggestion_message
        elif "MODERATE_YAWNING" in labels:
            suggestion_message = suggested_message_states[6]
            return suggestion_message
        
        
    return suggestion_message


def vehicleSpeedParamToggler(flag : bool = False,speed: int= None):
    
    if(flag):
        return speed
    else:
        speed = 6
        return speed

def alcoholParamToggler(flag : bool = False,mode: bool= False):
    if flag:
        return mode
    else:
        mode = False
        return mode


