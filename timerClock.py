# timer clock code goes here

import time,math


class clockTimer:
    def __init__(self):
        self.start_time = time.time()

    def getTimerCount(self,current_time):
        count = float(current_time-self.start_time)
        return math.floor(count)
        

    def resetTimer(self):
        self.start_time = time.time()