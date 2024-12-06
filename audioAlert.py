from pygame import mixer 
import time,random,cv2 

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

def playAlarm(state: str = "SAFE", seatbelt: str = "SEATBELT", terminate: bool = False):
    last_state = "SAFE"

    
    # Handle state change
    if last_state != state:
        if not channel2.get_busy(): 
            channel1.stop() 
            channel2.play(StateChange)
        last_state = state

        # Handle different states
    if state == "SAFE" :
        if channel1.get_busy():
            channel1.stop()  

    elif state == "PRECAUTION" and not channel1.get_busy():

        channel1.play(SlaveCaution,loops=100) 
            
    elif state == "CAUTION" and not channel1.get_busy():
            
        channel1.play(MasterCaution,loops=100) 
            
    elif state == "HAZARD" and not channel1.get_busy():

        channel1.play(HazardTone,loops=100) 

            
    # Simulate a loop delay
    time.sleep(0.1)

# Example Usage


        

    

def playSeatbeltWarn(play:True):

    if(play):
        channel2.play(SeatbeltWarn)
    else:
        channel2.play(Seatbelt)
        

    while play:
        if not channel2.get_busy():
            channel2.play()

        time.sleep(0.1)


    

# while True:
#     states = ["CAUTION","PRECAUTION","HAZARD"]
#     # terminate = False

#     choice = random.choice(states)

#     print("Choosen State",choice)

#     playAlarm(choice)
#     # time.sleep(4)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         # playAlarm("SAFE","NONE")
#         break





