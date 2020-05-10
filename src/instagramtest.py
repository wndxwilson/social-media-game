from instalooter.looters import HashtagLooter
import time
from datetime import datetime ,timedelta
import datetime as dt
# Data manipulation
import pandas as pd
import re


# Set the IG variables    
commonHT = 'hallxii' #standardised
allHT = ['hallxiitoxic' , 'hallxiimismatched', 'hallxiitiktok', 'hallxiicrossdres', 'hallxiifitspo']   
mainHT = 'xiithemeweek20'
todayHT = 'hallxiitoxic'

def extractNewPostsFromIG(todayHT):  
    #Search  hashtag
    looter = HashtagLooter(todayHT) #Assume extraction is once a day. Dw to do time v mafan
    
    # Create a df that contains new posts
    appendDF = pd.DataFrame(columns=['username','date', 'time', 'text', 'photo', 'is_video', 'points', 'hashtags'])
    index=0


    # Make each new post as a new row
    for onePost in looter.medias():    
        onePostDict= looter.get_post_info(onePost.get('shortcode'))  
        appendDF.at[index,'username'] = (onePostDict.get('owner')).get('username')
        appendDF.at[index,'date']= dt.datetime.utcfromtimestamp(int(onePostDict.get('taken_at_timestamp'))).strftime("%Y/%m/%d")
        appendDF.at[index,'time']=dt.datetime.utcfromtimestamp(int(onePostDict.get('taken_at_timestamp'))).strftime("%H:%M:%S")
        appendDF.at[index,'text'] = ((((onePostDict.get('edge_media_to_caption')).get('edges'))[0]).get('node')).get('text')
        appendDF.at[index,'photo'] = onePostDict.get('display_url')
        appendDF.at[index,'is_video'] = onePostDict.get('is_video') # returns True or False
        appendDF.at[index,'hashtags'] = todayHT  #this one go crawl from the other database
        
        index+=1
        
    # We will do sorting later
    return appendDF


def extractAllPostsFromIG(mainHT, commonHT,allHT):
    #Search hashtag
    looter = HashtagLooter(mainHT)
    
    # Create a df that contains new posts
    appendDF = pd.DataFrame(columns=['username','date', 'time', 'text', 'photo', 'is_video', 'hashtags'])
    index=0
    
    # Make each new post as a new row
    for onePost in looter.medias():    
        onePostDict= looter.get_post_info(onePost.get('shortcode'))    
        appendDF.at[index,'username'] = (onePostDict.get('owner')).get('username')
        appendDF.at[index,'date']= dt.datetime.utcfromtimestamp(int(onePostDict.get('taken_at_timestamp'))).strftime("%Y/%m/%d")
        appendDF.at[index,'time']=dt.datetime.utcfromtimestamp(int(onePostDict.get('taken_at_timestamp'))).strftime("%H:%M:%S")
        appendDF.at[index,'text'] = ((((onePostDict.get('edge_media_to_caption')).get('edges'))[0]).get('node')).get('text')
        appendDF.at[index,'photo'] = onePostDict.get('display_url')
        appendDF.at[index,'is_video'] = onePostDict.get('is_video') # returns True or False
        appendDF.at[index,'points'] = 0 #this one go crawl from the other database with HT
            
    # =============================================================================
    # If the single post contains more than one todayHT     
    # =============================================================================    
        text =  ((((onePostDict.get('edge_media_to_caption')).get('edges'))[0]).get('node')).get('text')
        
        totalPoints= 0 
        if (text.count(commonHT)>1): #many hashtags
            manyHT = [] # create a list to store a list of hashtags
            for HT in allHT: #loop through all the hashtags
                if HT in text:
                    manyHT.append(HT)
            appendDF.at[index,'points'] = totalPoints
            appendDF.at[index,'hashtags'] = manyHT 
            
        else: #one hashtag
            for HT in allHT: #loop through all the hashtags
                if HT in text:
                    appendDF.at[index,'hashtags'] = HT
        index+=1 
    
    # We will do sorting later
    return appendDF

print(extractNewPostsFromIG('hallxiitoxic'))