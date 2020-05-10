import pandas as pd

class Rewards():
    
    def __init__(self):
        self.data = pd.read_csv('tests.csv')

    def test(self):
        return self.data.sort_values(by=['points'], ascending=False)

if __name__ == '__main__':
    r = Rewards()
    a = r.test()
    for index, row in a.iterrows():
        print(row['name'], row['points'])
    print(r.test())