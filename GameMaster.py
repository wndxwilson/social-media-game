from random import sample, choice
from time import localtime, strftime

class GameMaster:
    def __init__(self):
        self.challengeslist = [x for x in range(50)]
        self.suddenMissionsList = [x for x in range(50, 100)]
        self.day = strftime("%w", localtime()) #Sunday is 0, Saturday is 6.
        self.forecast = {}
        self.suddenMissionForecast = {}
        self.__scheduleGames()
        self.__scheduleSuddenMissions()
        self.__dailyChallenges()
        self.__currentSuddenMission()


    def startGame(self):
        print("Works!")

    def __scheduleGames(self):
        for x in range(7):
            self.forecast[str(x)] = sample(self.challengeslist, 3)
        print("self.forecast:", self.forecast)

    def __scheduleSuddenMissions(self):
        suddenMission = sample(self.suddenMissionsList, 14)
        z = 0
        for x in range(7):
            for y in range(2):
                self.suddenMissionForecast[tuple([x, y])] = suddenMission[z]
                z = z+1
        print("self.suddenMissionForecast", self.suddenMissionForecast)

    def __dailyChallenges(self):
        print(self.forecast[self.day])

    def __currentSuddenMission(self):
        time = strftime("%H:%M:%S", localtime())
        period = 0
        if "15:00:00" <= time <= "23:59:59":
            period = 1
        print(self.suddenMissionForecast[tuple([int(self.day), period])])

if __name__=="__main__":
    gm = GameMaster()

