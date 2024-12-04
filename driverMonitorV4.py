#runner code goes here

import threading 
from configuration import getVideoFeed,getRealEmoText
from configuration import runStateProcessCounter
from configuration import LABEL,terminate
from audioAlert import playAlarm

thread1 = threading.Thread(target=getVideoFeed)
thread2 = threading.Thread(target=getRealEmoText)
thread3 = threading.Thread(target=runStateProcessCounter)
thread4 = threading.Thread(target=playAlarm,args=(LABEL,"SEATBELT",terminate))

thread1.start()
thread2.start()
thread3.start()

thread1.join()
thread2.join()
thread3.join()


