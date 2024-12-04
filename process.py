from timerClock import clockTimer
import time
from collections import deque
# clocktimer = clockTimer()


STATES = ["CAUTION","SAFE","HAZARD","DRIVER NOT FOUND"]
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


yawn_status_history = deque(maxlen=50)


def processData(dataDict: dict, counterOBJ,  vehicle_speed :int = 20 ):

    message_state = STATES[1]
    
    # print("Data dict--- ",dataDict)

    if dataDict['data']:
        
        eye_status = dataDict['eye_STATUS']
        head_pose = dataDict['currentHeadState']
        yawnAnalysisLog = dataDict['yawnAnalysisLog']
        left_eye = dataDict['left_eye']
        rigth_eye = dataDict['right_eye']



        if eye_status == "EYE_PRESENT" and  head_pose not in headpose_caution_states:
            count = 0
            counterOBJ.resetTimer()
            message_state = STATES[1]
            # suggested_message = processPassiveData(yawnAnalysisLog,"NOnE","NONE")
            return message_state,count

        elif(eye_status == "EYE_ABSENT" ):
            count = counterOBJ.getTimerCount(time.time())
            if count > 1 and count <= 4: 
                message_state = STATES[0]
            elif count > 4:
                message_state = STATES[2]

            # suggested_message = processPassiveData(yawnAnalysisLog,"NOnE","NONE")
            return message_state,count

        elif( eye_status == "EYE_ABSENT" and head_pose in headpose_caution_states ):
            count = counterOBJ.getTimerCount(time.time())

            if count > 1 and count <= 6 : 
                message_state = STATES[0]
            elif count > 6:
                message_state = STATES[2]

            # suggested_message = processPassiveData(yawnAnalysisLog,"NOnE","NONE")
            return message_state,count

        elif(head_pose in headpose_caution_states):
            count = counterOBJ.getTimerCount(time.time())

            if count > 1 and count <= 8: 
                message_state = STATES[0]
            elif count > 8:
                message_state = STATES[2]
            
            # suggested_message = processPassiveData(yawnAnalysisLog,"NOnE","NONE")
            return message_state,count
    else:
        count = counterOBJ.getTimerCount(time.time())

        if vehicle_speed > 5:
            if count > 2 and count <= 30: 
                message_state = STATES[3]
            elif count > 20:
                message_state = STATES[2]
        elif (vehicle_speed > 1 and vehicle_speed <= 5):
            if count > 60 : 
                message_state = STATES[2]
        
        # suggested_message = processPassiveData(yawnAnalysisLog,"NOnE","NONE")
        return message_state,count
        
    # if( left_eye['lhd'] == "DOWN" and rigth_eye == 'DOWN' ):
    #     if(len(yawnAnalysis.keys())>0):
    #         count = counterOBJ.getTimerCount(time.time())

    #         if count > 1 and count <= 6 : 
    #             message_state = STATES[0]
    #         elif count > 6:
    #             message_state = STATES[2]

    #         return message_state,count

# yawn_analysis = { 
#                     "yawnCountTF":yawnCountTF,
#                     "yawnLabel":yawnLabel,
#                     'timePeriodRun':timePeriodRun
#                 }


def processPassiveData(yawnAnalysis: dict , face_emotion:str , eye_tracking_data : str):

    global yawn_status_history

    suggestion_message = suggested_message_states[0]

    if(yawnAnalysis['yawnLabel'] == "SEVERE_YAWNING"):

        suggestion_message = suggested_message_states[2]
        return 


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