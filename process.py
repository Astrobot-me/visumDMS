from timerClock import clockTimer
import time
# clocktimer = clockTimer()


STATES = ["CAUTION","SAFE","HAZARD"]
# count = 0
headpose_caution_states = ['LOOKING_DOWN','FACE_DOWN','FACE_DOWN','BOTTOM_LEFT','BOTTOM_RIGHT']

def processData(eye_status: str, head_pose: str, counterOBJ ):

    message_state = STATES[1]
    

    if eye_status == "EYE_PRESENT" or  head_pose not in headpose_caution_states:
        count = 0
        counterOBJ.resetTimer()
        message_state = STATES[1]
        return message_state,count

    elif(eye_status == "EYE_ABSENT" ):
        count = counterOBJ.getTimerCount(time.time())
        if count > 0 and count <= 4: 
            message_state = STATES[0]
        elif count > 4:
            message_state = STATES[2]

        return message_state,count

    elif( eye_status == "EYE_ABSENT" and head_pose in headpose_caution_states ):
        count = counterOBJ.getTimerCount(time.time())

        if count > 0 and count <= 6 : 
            message_state = STATES[0]
        elif count > 6:
            message_state = STATES[2]

        return message_state,count

    elif(head_pose in headpose_caution_states):
        count = counterOBJ.getTimerCount(time.time())

        if count > 0 and count <= 8: 
            message_state = STATES[0]
        elif count > 8:
            message_state = STATES[2]
        
        return message_state,count