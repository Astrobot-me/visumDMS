#runner code goes here

import threading 
from configuration import getVideoFeed,getRealEmoText
from configuration import runStateProcessCounter


thread1 = threading.Thread(target=getVideoFeed)
thread2 = threading.Thread(target=getRealEmoText)
thread3 = threading.Thread(target=runStateProcessCounter)

thread1.start()
thread2.start()
thread3.start()

thread1.join()
thread2.join()
thread3.join()


