from pygame import mixer 
import time

# Initialize the mixer
mixer.init()


SeatbeltWarn = mixer.Sound("./resources/audio/tesla_seatbelt_warning.mp3")
Seatbelt = mixer.Sound("./resources/audio/tesla_seatbelt.mp3")

SlaveCaution = mixer.Sound("./resources/audio/precaution.mp3")
MasterCaution = mixer.Sound("./resources/audio/caution.mp3")
HazardTone = mixer.Sound("./resources/audio/alert.mp3")
StateChange = mixer.Sound("./resources/audio/tesla_seatbelt.mp3")


channel1 = mixer.Channel(0)
channel1.set_volume(1.0)

channel2 = mixer.Channel(1)
channel2.set_volume(1.0)

channel3 = mixer.Channel(2)

'''
possible states 
1: safe 
2: pre-caution 
3: caution 
4: hazard 


'''

def playAlarm(state: str = "SAFE",seatbelt = "SEATBELT",terminate: bool= False):

    last_state = "SAFE"

    while True:
        if not terminate:
            if(last_state != state):
                channel2.play(StateChange)
                last_state = state

            if(state == "SAFE"): 
                # state : 0
                pass
                # channel1.play(MasterCaution)
            elif(state == "PRECAUTION"):
                channel1.play(SlaveCaution)
            elif(state == "CAUTION"):
                channel1.play(MasterCaution)
            elif(state == "HAZARD"):
                channel1.play(HazardTone)

        

    

def playSeatbeltWarn(play:True):

    if(play):
        channel2.play(SeatbeltWarn)
    else:
        channel2.play(Seatbelt)
        

    while play:
        if not channel2.get_busy():
            channel2.play()

        time.sleep(0.1)


    
