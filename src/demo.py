from instagramtest import*
from googletest import*

from instalooter.looters import HashtagLooter
import time
from datetime import datetime ,timedelta
import datetime as dt
# Data manipulation
import pandas as pd
import re

print(dt.datetime.today()strftime("%Y/%m/%d"))
'''
nameList = extractAllDataFromGS("UserInfo")
hashtag = extractAllDataFromGS("Challenges").sample(n=5)
for index, ht in hashtag.iterrows():
    df = extractNewPostsFromIG(ht['Hashtag'])
    for index, row in df.iterrows():
        if(nameList['username'].str.contains(row['username']))
            add
        '''