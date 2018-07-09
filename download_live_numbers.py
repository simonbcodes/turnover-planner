from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import config
import pandas as pd
from sklearn.externals import joblib

#adapted from the quickstart.py file found on the Google API Sheets website

# Setup the Sheets API
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

# Call the Sheets API
SPREADSHEET_ID = config.spreadsheet_id
RANGE_NAME = 'Script!A1:H200'
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])
if not values:
    print('No data found.')
else:
    classes = pd.DataFrame(columns=values[0])
    # print(type(values))
    for row in values:
       # print('{} - {} - {} - {} - {} - {} - {} - {}'.format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
       # print('{} - {} - {} - {} - {} - {} - {} - {}'.format(values[0][0], values[0][1], values[0][2], values[0][3], values[0][4], values[0][5], values[0][6], values[0][7]))
       classes = classes.append({str(values[0][0]): row[0], str(values[0][1]): row[1], str(values[0][2]): row[2], str(values[0][3]): row[3], str(values[0][4]): row[4], str(values[0][5]): row[5], str(values[0][6]): row[6], str(values[0][7]): row[7]}, ignore_index=True)
    print(classes)
    joblib.dump(classes, 'live_numbers.pkl')
