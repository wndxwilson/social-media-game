'''References
https://towardsdatascience.com/accessing-google-spreadsheet-data-using-python-90a5bc214fd2
https://instalooter.readthedocs.io/en/latest/instalooter/index.html
'''
# =============================================================================
# Import libraries
# =============================================================================
# Google sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Data manipulation
import pandas as pd
import re

# Instagram
from instalooter.looters import HashtagLooter
import time
import datetime as dt

# =============================================================================
# Variables setting    
# =============================================================================

# Authentication via Google API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)

#Set the GS variables
searchValue = 'ntuhall12' #exact match 
sheetName = 'DailyChallenges'
rowOne = ["I'm","inserting","a","new","row","into","a,","Spreadsheet","using","Python"]

# Set the IG variables    
commonHT = 'hallxii' #standardised
allHT = ['hallxiitoxic' , 'hallxiimismatched', 'hallxiitiktok', 'hallxiicrossdres', 'hallxiifitspo']   
mainHT = 'xiithemeweek20'
todayHT = 'hallxiitoxic'
    
'''
Run variables setting and Functions Calling First
'''
# No return variables
appendRowToGS(sheetName, rowOne)
appendManyRowsToGS(sheetName, rowDF)
checkUsernameExistInGS('Players','@vhkbewmw')
updateCellToGS(sheetName,1, 2, "telemedicine_id") #rowIndex = 1, colIndex = 2
updatePlayerPointsToGS('Players', '@vhkbewmw', 50) 

# With return variables

#GS
cell_list = findCellLocation(sheetName, searchValue)
df = extractAllDataFromGS('DailyChallenges')
todayChallengeDF = extractTodayChallengeFromGS('Challenges','2020/05/14')
todayPoints = extractTodayPointsFromGS('DailyChallenges', todayHT)

#IG
newPosts = extractNewPostsFromIG(todayHT)    
allPosts = extractAllPostsFromIG(mainHT, commonHT,allHT)

# =============================================================================
# Functions calling
# =============================================================================
# Google Sheets
# =============================================================================

def appendRowToGS(sheetName,rowOne): # one row
    getSheet = client.open(sheetName).sheet1
    getSheet.append_row(rowOne)

def appendManyRowsToGS(sheetName,rowDF): #add new players, add todayChallenge to Challenges by Players    
    getSheet = client.open(sheetName).sheet1
    
    colNames = list(rowDF.columns.values)
    for col in colNames: #Need to change datatype to str
        rowDF[col] = rowDF[col].astype('str') 
    rowLists = rowDF.values.tolist()
    for row in rowLists:
        getSheet.append_row(row)


def checkUsernameExistInGS(sheetName, username):
    getSheet = client.open(sheetName).sheet1
    try:
        cell = getSheet.find(username)
        return cell
    except:
        return "Username not found"
    
def updateCellToGS(sheetName,rowIndex, colIndex, updateValue): 
    getSheet = client.open(sheetName).sheet1
    getSheet.update_cell(rowIndex, colIndex, updateValue)

def updatePlayerPointsToGS(sheetName, username, points):
    getSheet = client.open(sheetName).sheet1
    cell = getSheet.find(username)
    getSheet.update_cell(cell.row, cell.col +1 , points)   
    
def extractAllDataFromGS(sheetName):
    getSheet = client.open(sheetName).sheet1
    getAllValues= getSheet.get_all_values()
    allDF = pd.DataFrame(getAllValues)
    allDF.columns = allDF.iloc[0] # Set first row as column header
    allDF = allDF[1:] # Remove first row as it has become a column header

    return allDF

def extractTodayChallengeFromGS(sheetName,date):
    getSheet = client.open(sheetName).sheet1
    cell = getSheet.find(date)
    listChallenge = getSheet.row_values(cell.row)
    df = pd.DataFrame(listChallenge)
    df= df.T #transpose
    df =df.rename(columns={0: "username", 1: "description", 2: "hashtags", 3: "points", 4: "date"})
    
    return df

def extractTodayPointsFromGS(sheetName, todayHT):
    getSheet = client.open(sheetName).sheet1
    cell = getSheet.find(todayHT) #Find a cell with exact string value
    pointsInDoubleList =str(getSheet.get('D' + str (cell.row))) # It will return a value like [['40']] , so we need to remove [[]] and turn it into integers
    pointsLeftRemove = pointsInDoubleList.replace('[[','') #'40']]
    pointsSingleQuote= pointsLeftRemove.replace(']]','') #'40'
    pointsString = pointsSingleQuote.replace("'", "") #40
    todayPoints = int(pointsString)

    return todayPoints

def findCellLocation(sheetName, searchValue): 
    getSheet = client.open(sheetName).sheet1
    cell = getSheet.findall(searchValue) # Lazy to clean ah, let me know if need it
    return cell

# =============================================================================
# Instagram 
# =============================================================================    
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
        appendDF.at[index,'points'] = extractTodayPointsFromGS('DailyChallenges', todayHT) # From Google Sheets
        appendDF.at[index,'hashtags'] = todayHT  #this one go crawl from the other database
        
        index+=1
        
    # We will do sorting later
    return appendDF


def extractAllPostsFromIG(mainHT, commonHT,allHT):
    #Search hashtag
    looter = HashtagLooter(mainHT)
    
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
                    pointsHT = extractTodayPointsFromGS('DailyChallenges', HT)
                    totalPoints += pointsHT
            appendDF.at[index,'points'] = totalPoints
            appendDF.at[index,'hashtags'] = manyHT 
            
        else: #one hashtag
            for HT in allHT: #loop through all the hashtags
                if HT in text:
                    appendDF.at[index,'hashtags'] = HT
                    pointsHT = extractTodayPointsFromGS('DailyChallenges', HT)
                    appendDF.at[index,'points'] = pointsHT
        index+=1 
    
    # We will do sorting later
    return appendDF


