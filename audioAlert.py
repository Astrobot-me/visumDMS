from pygame import mixer 
import time

# Initialize the mixer
mixer.init()


SeatbeltWarn = mixer.Sound("./resources/audio/tesla_seatbelt_warning.mp3")
Seatbelt = mixer.Sound("./resources/audio/tesla_seatbelt.mp3")
MasterCaution = mixer.Sound("./resources/audio/alert.mp3")
HazardTone = mixer.Sound("./resources/audio/alert.mp3")


channel1 = mixer.Channel(0)
channel1.set_volume(1.0)

channel2 = mixer.Channel(1)
channel2.set_volume(1.0)

channel3 = mixer.Channel(2)

def playAlarm(state: int,seatbelt = "SEATBELT"):
    if(state == 0):
        pass
        # channel1.play(MasterCaution)
    elif(state == 1):
        channel1.play(MasterCaution)
    elif(state == 2):
        channel3.play(HazardTone)

    # if(seatbelt == "SEATBELT"):
    #     playSeatbeltWarn(True)
    # else:
    #     pass


def playSeatbeltWarn(play:True):

    if(play):
        channel2.play(SeatbeltWarn)
    else:
        channel2.play(Seatbelt)
        

    while play:
        if not channel2.get_busy():
            channel2.play()

        time.sleep(0.1)


    
