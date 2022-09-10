import os.path
import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import bukken
from enum_priority import Priority
from homescojp_scrapper import HomescoojpScrapper as scrapper
import yahoo_norikae_scrap as yns
from dict_destinations import destinations


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
DATA_TO_PULL = '1b7b5a74pHrAqkd3OdLA83ydJSLutQonDO_Yf-XAWNo0'
SHEET_RANGE_NAME = 'House and info (auto)!A:S'

class SheetHandler:

    def __init__(self) -> None:
        self.df_base = pd.DataFrame()
        self.df_output = pd.DataFrame()

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

            pd.DataFrame(values).to_csv('data.csv')
        except HttpError as err:
            print(err)

    def initiate_df(self):
        if not os.path.exists('data.csv'):
            self.download_spreadsheet()
        else:
            print("file already exists")
        self.df_base = pd.read_csv('data.csv')


    def loop_through_rows(self, gmh):
        # TODO refactor/extract in better way
        """Go through each row and scrap and calcualte required info

        Args:
            gmh (GoogleMapsHandler): handler for Google location APIs
        """
        for row_idx in range(1, len(self.df_base)):
            # Create a new bukken
            current_bukken = bukken.Bukken()
            # Get link from sheet (index 2)
            link = self.df_base.iloc[row_idx][2]
            current_bukken.listing_link = link
            # Fill bukken with scrapping data
            scrapper(link).scrap_all(current_bukken)
            current_bukken.address_jp = gmh.reverse_geocode_jp(current_bukken.coordinates)
            items_to_add = current_bukken.extract()

            for destination in destinations.values():
                items_to_add.append(yns.lookup_time_transfers(current_bukken.address_jp, destination, priority=Priority.Convenient.value))
            new_row = pd.Series(items_to_add)
            self.df_output = self.df_output.append(new_row, ignore_index=True)

if __name__ == '__main__':
    # Only run spreadsheet reading if data doesn't exist to avoid unless API calls
    sh = SheetHandler()
    sh.initiate_df()
    sh.loop_through_rows()
    