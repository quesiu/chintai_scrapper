import bukken
from google_maps_handler import GoogleMapsHandler
import homescojp_scrapper
from sheets_handler import SheetHandler
import yahoo_norikae_scrap
from dict_destinations import destinations

# for name, address in destinations.items():
#     print(f'{name} - {address}')

def fill_sheet_with_info():
    # Initialize different objects
    gmh = GoogleMapsHandler()
    sh = SheetHandler()

    sh.initiate_df()
    sh.loop_through_rows(gmh)
    sh.upload_sheet()
    # sh.df_output.to_csv('output.csv', index=False, header=False)

if __name__ == '__main__':
    fill_sheet_with_info()
    print('Succesfully output data')