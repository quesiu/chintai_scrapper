from enum_priority import Priority
from google_maps_handler import GoogleMapsHandler
from sheets_handler import SheetHandler

def fill_sheet_with_info():
    # TODO: Refactor with Sheets Handler
    """Main function that initialize and run all scripts
    """
    # Initialize different objects
    gmh = GoogleMapsHandler()
    sh = SheetHandler()

    sh.initiate_df()
    sh.loop_through_rows(gmh, priority=Priority.Convenient.value)
    # sh.upload_sheet()
    sh.df_output.to_csv('output.csv', index=False, header=False)

if __name__ == '__main__':
    fill_sheet_with_info()
    print('Succesfully output data')