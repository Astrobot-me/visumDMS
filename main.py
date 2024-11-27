#runner code goes here

import threading 
from configuration import getVideoFeed,getRealEmoText


thread1 = threading.Thread(target=getVideoFeed)
thread2 = threading.Thread(target=getRealEmoText)

thread1.start()
thread2.start()

thread1.join()
thread2.join()


