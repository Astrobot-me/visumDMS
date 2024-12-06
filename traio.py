analysisDict = {
                "emotiondict": 1,
                "dominantemotion": 1,
                "face_confidence": 2,
                "age": 3,
                "dominant_gender": 5,
                "leye_region": 5,
                "reye_region": 6
            }

print(analysisDict['dominantemotion'])


li = ['a','b']

if 'a' not in li :
    print("Hellow world")
else: 
    print("Relax world")

size = 2
array = ["hello","feloo"]
if(size>1):
    for i in range(size-1,-1,-1):
        print(array[i])


print(len({}.keys()))        

from pygame import mixer 
import time,random

# Starting the mixer 
mixer.init() 

# Loading the song 
mixer.music.load("./resources/audio/alert.mp3") 

# Setting the volume 
mixer.music.set_volume(1) 

# Start playing the song 
# mixer.music.play() 

# Infinite loop for user interaction
# while True: 
#     print("Press 'p' to pause, 'r' to replay from the start") 
#     print("Press 'e' to exit the program") 
#     query = input(" ").strip().lower()  # Convert input to lowercase and remove extra spaces
    
#     if query == 'p': 
#         # Pausing the music 
#         mixer.music.pause()	      
#     elif query == 'r': 
#         # Rewind and replay the music 
#         mixer.music.rewind() 
#         mixer.music.play()
#     elif query == 'e': 
#         # Stop the mixer and exit
#         mixer.music.stop() 
#         break
#     else:
#         print("Invalid input. Please try again.")

# Load the first audio file
audio1 = mixer.Sound("./resources/audio/alert.mp3") 

# Load the second audio file
audio2 = mixer.Sound("./resources/audio/tesla_seatbelt.mp3") 
audio3 = mixer.Sound("./resources/audio/precaution.mp3") 
audio4 = mixer.Sound("./resources/audio/caution.mp3") 

# Play both audio files on different channels
channel1 = mixer.Channel(0)  # First audio on channel 0
channel2 = mixer.Channel(1)  # Second audio on channel 1

channel1.play(audio1)
channel2.play(audio2)

# Infinite loop for user interaction
while True: 
    print("Press 'p' to pause both audios, 'r' to replay both from the start") 
    print("Press 'e' to exit the program") 
    # query = input(" ").strip().lower()

    

    query = random.choice(['c','p','h'])

    # time.sleep(1)
    print("Replaying with query : ",query)
    if query == 'p' and not channel1.get_busy(): 

        channel1.stop()
        channel2.stop()
        channel1.play(audio3)
        channel2.play(audio2)
    elif query == 'h' and not channel1.get_busy(): 
        # Rewind and replay both audios
        channel1.stop()
        channel2.stop()
        channel1.play(audio1)
        channel2.play(audio2)
    elif query == 'c' and not channel1.get_busy(): 
        # Rewind and replay both audios
        channel1.stop()
        channel2.stop()
        channel1.play(audio4)
        channel2.play(audio2)
    elif query == 'e': 
        # Stop both audios and exit
        channel1.stop()
        channel2.stop()
        break
    else:
        print("Invalid input. Please try again.") 

    time.sleep(1)

