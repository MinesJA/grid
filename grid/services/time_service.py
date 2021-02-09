import time

class TimeService():

    def __init__(self):
        self.timer_start = False #Should be a singleton

    def start(self):
        self.timer_start = True
        try:
            while self.timer_start:
                print(time.ctime())
                time.sleep(1)
        except KeyboardInterrupt:
            print('interrupted!')
    
    def stop(self):
        self.timer_stop = False
        