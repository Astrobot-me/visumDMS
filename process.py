from timerClock import clockTimer
import time
clocktimer = clockTimer()


STATES = ["CAUTION","SAFE","HAZARD"]
count = 0
headpose_caution_states = ['LOOKING_DOWN','FACE_DOWN','FACE_DOWN','BOTTOM_LEFT','BOTTOM_RIGHT']

def processData(eye_status: str, head_pose: str ):

    clocktimer.resetTimer()
    message_state = STATES[1]
    count = 0

    if eye_status == "EYE_PRESENT" :
        # count = 0
        clocktimer.resetTimer()
        message_state = STATES[1]
        return message_state

    elif( eye_status == "EYE_ABSENT" and head_pose in headpose_caution_states ):
        count = clocktimer.startTimer(time.time())

        if count > 6: 
            message_state = STATES[0]
        elif count > 10:
            message_state = STATES[2]

        return message_state

    elif(head_pose in headpose_caution_states):
        count = clocktimer.startTimer(time.time())

        if count > 6: 
            message_state = STATES[0]
        elif count > 10:
            message_state = STATES[2]
        
        return message_state