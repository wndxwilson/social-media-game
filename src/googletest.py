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


def save(sheetName,data):
    getSheet = client.open(sheetName).sheet1
    getSheet.update([data.columns.values.tolist()] + data.values.tolist())



