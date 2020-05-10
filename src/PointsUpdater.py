from re import search
from random import randint
from googletest import*
class PointsUpdater:
    def __init__(self, participant):
        self.participant = participant
        self.points = randint(0, 101)
        self.rewardTier = {(0, 50): "Nothing", (51, 75): "A bear", (76, 100): "A trip to Sentosa"}

    def updatePoints(self, hashtag, ig_caption):
        hashtag = r"{}".format(hashtag)
        if search(hashtag, ig_caption):
            self.points = self.points + 1
        print(self.points)
    
    def claimReward(self):
        temp_dict = list(self.rewardTier.keys())
        for x in range(len(temp_dict)):
            minimum, maximum = temp_dict[x]
            if minimum <= self.points <= maximum:
                print(self.rewardTier[temp_dict[x]])

    def addPoints(self, points):
        self.points = self.points + points
        print(self.points) 

    def removePoints(self, points):
        self.points = self.points - points
        print(self.points)

if __name__ == "__main__":
    pu = PointsUpdater("Jenny")
    print(pu.participant)
    print(pu.points)
    pu.addPoints(1)
    pu.removePoints(1)
    pu.updatePoints("#code4Corona", "Yay, I have just joined #code4Corona!!!")
    pu.claimReward()

