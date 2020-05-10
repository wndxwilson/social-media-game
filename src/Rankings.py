from random import choice, sample, randint
import string
from googletest import*


def randomString():
    letters = string.ascii_lowercase
    return ''.join(choice(letters) for i in range(8))

class Rankings:
    def __init__(self):
        self.list_of_players = [randomString() for x in range(20)]
        self.all_scores = {}
        for x in self.list_of_players:
            self.all_scores[x] = randint(0, 101)
        self.friends_list = sample(self.list_of_players, 10)
        print(self.list_of_players)
        print(self.all_scores)
        print(self.friends_list)
        self.nameList = extractAllDataFromGS("UserInfo")

        
    def display():
        ranking = "LeaderBoard Rankings\n"
        for index, row in self.nameList.iterratrow():
            ranking += row['username']+" : "+row['points']
            ranking += "\n"
            
        
    def displayRankings(self):
        list_of_scores = []
        for x in self.list_of_players:
            list_of_scores.append(self.all_scores[x])
        unique_scores = list(set(list_of_scores))
        unique_scores.sort(reverse = True)
        top_three = {"1st": [], "2nd": [], "3rd": []}
        for x in self.list_of_players:
            if self.all_scores[x] == unique_scores[0]:
                top_three["1st"].append(x)
            elif self.all_scores[x] == unique_scores[1]:
                top_three["2nd"].append(x)
            elif self.all_scores[x] == unique_scores[2]:
                top_three["3rd"].append(x)
        print(list_of_scores)
        print(unique_scores)
        print(top_three)
        return self.all_scores

    def displayFriendRankings(self):
        list_of_scores = []
        for x in self.friends_list:
            list_of_scores.append(self.all_scores[x])
        unique_scores = list(set(list_of_scores))
        unique_scores.sort(reverse = True)
        top_three = {"1st": [], "2nd": [], "3rd": []}
        for x in self.friends_list:
            if self.all_scores[x] == unique_scores[0]:
                top_three["1st"].append(x)
            elif self.all_scores[x] == unique_scores[1]:
                top_three["2nd"].append(x)
            elif self.all_scores[x] == unique_scores[2]:
                top_three["3rd"].append(x)
        print(list_of_scores)
        print(unique_scores)
        print(top_three)

if __name__ == "__main__":
    rk = Rankings()
    rk.displayRankings()
    rk.displayFriendRankings()