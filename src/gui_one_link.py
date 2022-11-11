from typing import Tuple
import streamlit as st
import pandas as pd
from google_maps_handler import GoogleMapsHandler
from sheets_handler import SheetHandler

LAT_LONG_REGEX = r'{\"lat\":\"(\d*\.\d*)\",\"lng\":\"(\d*.\d*)\"}'

def fill_dataframe_with_info(url:str) -> pd.DataFrame:
    # TODO: Refactor with Sheets Handler
    """Main function that initialize and run all scripts
    """
    # Initialize different objects
    gmh = GoogleMapsHandler()
    sh = SheetHandler()

    sh.initiate_df(url)
    sh.loop_through_rows(gmh)
    # sh.upload_sheet()
    # sh.df_output.to_csv('output_one.csv', index=False, header=False, encoding='utf-8-sig')    
    # sh.df_output.to_clipboard(False, index=False, header=False, encoding='utf-8')
    return sh.df_output

def generate_gui():
    st.title('Result')
    url_input = st.text_input(label="Paste property URL page below")
    st.button("Analyze property", on_click=display_results, args=[url_input])

def display_results(url_input:str):
    print(f'{url_input} is of type {type(url_input)}')
    if url_input is None or url_input is '':
        url_input = 'https://www.afr-web.co.jp/hebel-rooms/search/detail/?clientcorp_room_cd=B201334160402'
    df = fill_dataframe_with_info(url_input)
    df = add_custom_headers(df)
    # Display DataFrame as table using streamlit
    st.write(df)
    generate_map(df)

def extract_coordinates(df) -> Tuple[str,str]:
    map_link = df.loc[0].at["Maps"]
    longi = map_link[34:49]
    lati = map_link[52:]
    return (lati, longi)

def add_custom_headers(df:pd.DataFrame) -> pd.DataFrame:
    headers =  ["Name", "Link", "Address", "Maps", "Monthly price", "Surface (m2)", "Price/m2", "Age", "Type", "Shape", "Closest stations", "Amita Kanda", "MCP Otemachi", "Shinagawa", "XTIA", "Recursive Ebisu", "Ikebukuro", "Musashi Urawa", "Amita Kanda2", "MCP Otemachi2", "Shinagawa2", "XTIA2", "Recursive Ebisu2", "Ikebukuro2", "Musashi Urawa2"]
    df.columns = headers
    return df

def generate_map(df:pd.DataFrame):
    # lati, longi = coordinates
    data = pd.DataFrame(
        {   'Name': [df.loc[0].at['Name']],
            'Link': [df.loc[0].at['Link']],
            'latitude': [float(df.loc[0].at["Maps"][34:49])],
            'longitude': [float(df.loc[0].at["Maps"][52:])]
        })
    st.map(data = data)
#     st.deck_gl_chart(
#             viewport={
#                 'latitude': lati,
#                 'longitude':  longi,
#                 'zoom': 10
#             },
#             layers=[{
#                 'type': 'ScatterplotLayer',
#                 'data': data,
#                 'radiusScale': 250,
#    'radiusMinPixels': 5,
#                 'getFillColor': [248, 24, 148],
#             }]
#         )


if __name__ == '__main__':
    # df = fill_sheet_with_info('https://www.afr-web.co.jp/hebel-rooms/search/detail/?clientcorp_room_cd=B201334160402')
    generate_gui()
    print('Succesfully output data')