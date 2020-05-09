'''References
https://towardsdatascience.com/accessing-google-spreadsheet-data-using-python-90a5bc214fd2
''''
# =============================================================================
# Import libraries
# =============================================================================
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# =============================================================================
# Authentication via Google API
# =============================================================================
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)

# =============================================================================
# Get data from Google Sheet
# =============================================================================
getSheet = client.open('testing').sheet1
#sheetURL = client.open_by_url('https://docs.google.com/spreadsheets/d/1siC_mThGYtPTOroVlw7jefGqG595Q7nfE6G2HN0CCSY/edit?usp=sharing') # Get URL

print(getSheet.get('A1')) # Get A1 
#print(getSheet.sheet1.get('A1')) # Get A1 

# Get the whole data from the sheet
getAllValues= getSheet.get_all_values()
df = pd.DataFrame(getAllValues)

# Convert from sheets to dataframe
#df.columns = df.iloc[0] # Set first row as column header
#df = df[1:] # Remove first row as it has become a column header

# =============================================================================
# Append data to Google Sheet
# =============================================================================
row = ["I'm","inserting","a","new","row","into","a,","Spreadsheet","using","Python"]
getSheet.append_row(row)

#row 1, column 2
getSheet.update_cell(1, 2, "telemedicine_id")