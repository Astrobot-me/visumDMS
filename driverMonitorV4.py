#runner code goes here

import threading 
from configuration import getVideoFeed
from configuration import runStateProcessCounter
from configuration import LABEL,terminate
from audioAlert import playAlarm
from configuration import logIntoDb
from locationServer import start_location_thread


thread1 = threading.Thread(target=getVideoFeed)
# thread2 = threading.Thread(target=getRealEmoText)
thread3 = threading.Thread(target=runStateProcessCounter)
thread_location = threading.Thread(target=start_location_thread,daemon=True)
thread4 = threading.Thread(target=logIntoDb)




thread1.start()
# thread2.start()
thread3.start()
thread_location.start()
thread4.start()


thread1.join()
# thread2.join()
thread3.join()
thread4.join()



