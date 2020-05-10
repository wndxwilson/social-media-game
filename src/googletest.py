# =============================================================================
# Import libraries
# =============================================================================
# Google sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Data manipulation
import pandas as pd
import re

# Authentication via Google API
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)

def extractAllDataFromGS(sheetName):
    getSheet = client.open(sheetName).sheet1
    getAllValues= getSheet.get_all_values()
    allDF = pd.DataFrame(getAllValues)
    allDF.columns = allDF.iloc[0] # Set first row as column header
    allDF = allDF[1:] # Remove first row as it has become a column header

    return allDF

def checkUsernameExistInGS(sheetName, username):
    getSheet = client.open(sheetName).sheet1
    try:
        cell = getSheet.find(username)
        return True
    except:
        return False

def save(sheetName,data):
    getSheet = client.open(sheetName).sheet1
    getSheet.update([data.columns.values.tolist()] + data.values.tolist())

def extractTodayPointsFromGS(sheetName, user):
    getSheet = client.open(sheetName).sheet1
    cell = getSheet.find(user) #Find a cell with exact string value
    pointsInDoubleList =str(getSheet.get('C' + str (cell.row))) # It will return a value like [['40']] , so we need to remove [[]] and turn it into integers
    pointsLeftRemove = pointsInDoubleList.replace('[[','') #'40']]
    pointsSingleQuote= pointsLeftRemove.replace(']]','') #'40'
    pointsString = pointsSingleQuote.replace("'", "") #40
    todayPoints = int(pointsString)

    return todayPoints

def updatePlayerPointsToGS(sheetName, username, points):
    getSheet = client.open(sheetName).sheet1
    cell = getSheet.find(username)
    getSheet.update_cell(cell.row, cell.col +2 , points)   

def extractTodayChallengeFromGS(sheetName,date):
    getSheet = client.open(sheetName).sheet1
    cell = getSheet.find(date)
    listChallenge = getSheet.row_values(cell.row)
    df = pd.DataFrame(listChallenge)
    df= df.T #transpose
    df =df.rename(columns={0: "username", 1: "description", 2: "hashtags", 3: "points", 4: "date"})
    
    return df