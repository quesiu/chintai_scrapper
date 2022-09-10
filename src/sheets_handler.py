import os.path
import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
DATA_TO_PULL = '1b7b5a74pHrAqkd3OdLA83ydJSLutQonDO_Yf-XAWNo0'
SHEET_RANGE_NAME = 'Test Retool!A:S'

class SheetHandler:

    def __init__(self) -> None:
        self.df = pd.DataFrame.empty

    def download_spreadsheet(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('sheets', 'v4', credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=DATA_TO_PULL,
                                        range=SHEET_RANGE_NAME).execute()
                                        # ).execute()
            values = result.get('values', [])

            if not values:
                print('No data found.')
                return

            self.df = pd.DataFrame(values)
            self.df.to_csv('data.csv')
        except HttpError as err:
            print(err)

if __name__ == '__main__':
    # Only run spreadsheet reading if data doesn't exist to avoid unless API calls
    if not os.path.exists('data.csv'):
        sh = SheetHandler()
        sh.download_spreadsheet()
        pass
    else:
        print("file already exists")
    