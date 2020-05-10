
import schedule 
import time 
class scheduler():

    def __init__(self):
        self.b = False

    def start(self):
        try:
            self.b = True
            schedule.every(1).minutes.do(self.ping) 
            while self.b: 
  
                # Checks whether a scheduled task  
                # is pending to run or not 
                schedule.run_pending() 
                time.sleep(1) 

        except Exception as e:
            print("sendMenuPeriodically: "+str(e)+"\n")

    def ping(self):
        print("works")
    def stop(self):
        self.b = False



s = scheduler()
s.start()