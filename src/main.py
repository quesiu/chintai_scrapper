from google_maps_handler import GoogleMapsHandler
from dataframe_handler import DataFrameHandler

def fill_dataframe_with_info():
    # TODO: Refactor with DataFrameHandler
    """Main function that initialize and run all scripts
    """
    # Initialize different objects
    gmh = GoogleMapsHandler()
    dfh = DataFrameHandler()

    dfh.initiate_df()
    dfh.loop_through_rows(gmh)
    # sh.upload_sheet()
    dfh.df_output.to_csv('output.csv', index=False, header=False, encoding='utf-8-sig')

if __name__ == '__main__':
    fill_dataframe_with_info()
    print('Succesfully output data')