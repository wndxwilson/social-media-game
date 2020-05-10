from random import sample, choice
from time import localtime, strftime
from googletest import*
from instagramtest import*

import schedule 
import time 

class GameMaster:
    def __init__(self):
        self.challengeslist = [x for x in range(50)]
        self.suddenMissionsList = [x for x in range(50, 100)]
        self.day = strftime("%w", localtime()) #Sunday is 0, Saturday is 6.
        self.forecast = {}
        self.suddenMissionForecast = {}
        self.__scheduleSuddenMissions()
        self.__currentSuddenMission()
        self.b = False
        self.dailychallenge = None
        self.data = extractAllDataFromGS("Challenges")
        self.nameList = extractAllDataFromGS("UserInfo")



    def startGame(self):
        try:
            self.b = True
            if(self.dailychallenge == none):
                self.scheduleGames()
            schedule.every().day.at("00:00").do(self.scheduleGames)
            schedule.every(2).minutes.do(self.__scheduleSuddenMissions)
            schedule.every(2).minutes.do(self.updatepoints)
            while self.b: 
  
                # Checks whether a scheduled task  
                # is pending to run or not 
                schedule.run_pending() 
                time.sleep(1) 
        except Exception as e:
            print("sendMenuPeriodically: "+str(e)+"\n")

    def stopGame(self):
        self.b = False

    def scheduleGames(self):
        self.dailychallenge = self.data.sample(n=5)
        print(self.dailychallenge)

    def __scheduleSuddenMissions(self):
        suddenMission = sample(self.suddenMissionsList, 14)
        z = 0
        for x in range(7):
            for y in range(2):
                self.suddenMissionForecast[tuple([x, y])] = suddenMission[z]
                z = z+1
        print("self.suddenMissionForecast", self.suddenMissionForecast)

    def updatepoints(self):
        for index, dc in self.dailychallenge.iterrows():
             df = extractNewPostsFromIG(dc['Hashtag'])
            for index, row in df.iterrows():
                if(nameList['username'].str.contains(row['username']))
                    addPoints(self,nameList['username'],nameList['points'])


    def addPoints(self,username,points):
        self.nameList.loc[self.nameList.username == username, 'points'] =  int(self.nameList.loc[self.nameList.username == username, 'points'].values) + points
        save("UserInfo",self.nameList)

    def __currentSuddenMission(self):
        time = strftime("%H:%M:%S", localtime())
        period = 0
        if "15:00:00" <= time <= "23:59:59":
            period = 1
        print(self.suddenMissionForecast[tuple([int(self.day), period])])

if __name__=="__main__":
    gm = GameMaster()
    gm.startGame()

