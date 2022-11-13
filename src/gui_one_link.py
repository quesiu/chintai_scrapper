from typing import Tuple
import json
import io
import streamlit as st
import pandas as pd
import pydeck as pdk
from streamlit_option_menu import option_menu
# Custom libraries
from google_maps_handler import GoogleMapsHandler
from dataframe_handler import DataFrameHandler

# LAT_LONG_REGEX = r'{\"lat\":\"(\d*\.\d*)\",\"lng\":\"(\d*.\d*)\"}'
ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/0/01/Geokey.svg"

def fill_dataframe_with_info(url:str) -> pd.DataFrame:
    # TODO: Refactor with Sheets Handler
    """Main function that initialize and run all scripts
    """
    # Initialize different objects
    gmh = GoogleMapsHandler()
    sh = DataFrameHandler()

    sh.initiate_df(url)
    sh.loop_through_rows(gmh)
    # sh.upload_sheet()
    # sh.df_output.to_csv('output_one.csv', index=False, header=False, encoding='utf-8-sig')    
    # sh.df_output.to_clipboard(False, index=False, header=False, encoding='utf-8')
    return sh.df_output

def generate_gui():
    selected = option_menu(None, ["Home", 'Settings'], 
        icons=['house', 'gear'],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal")
    selected
    if selected == 'Home':
        generate_home()
    elif selected == 'Settings':
        generate_settings()
    else:
        print("Error: not possible to display current page")
    # display_results(url_input)

def generate_home():
    url_input = st.text_input(label="Paste property URL page below")
    st.button("Analyze property", on_click=display_results, args=[url_input])

def generate_settings():
    # TODO: refactor file check in a better way
    try:
        with open('config_chintai.json', 'r+') as f:
            config = json.loads(f.read())
            generate_each_config(config)
    except FileNotFoundError:
        with open('config_chintai.json', 'w+') as f:
            print("config_chintai.json doesn't exist yet, creation of new file with default settings")
            init_json_config(f)

def generate_each_config(config:dict):
    # Loop through all elements to display them as parameters
    for key, value in config.items():
        if type(value) is dict:
            st.header(key)
            generate_each_config(value)
            pass
        if type(value) is bool:
            st.checkbox(label=key, value=value)
            pass
        if type(value) is int or type(value) is float:
            st.number_input(label=key, value=value)
            

def init_json_config(f:io.TextIOWrapper) -> str:
    # TODO: refactor in its own class or something more appropriate
    init_conf = {
        'transit_fast': True,
        'transit_cheap': False,
        'transit_convenient': True,
        'conditional_formatting': {
            'monthly_price_cf': {
                'dark_red': 260000,
                'red': 240000,
                'orange': 220000,
                'blue_green': 200000,
            },
            'surface_cf': {
                'dark_red': 40,
                'red': 45,
                'orange': 50,
                'blue_green': 55,
            },
            'price_m2_cf': {
                'dark_red': 5000,
                'red': 4500,
                'orange': 4000,
                'blue_green': 3500,
            }
        }
    }
    return json.dump(init_conf, f)

def display_results(url_input:str):
    # print(f'{url_input} is of type {type(url_input)}')
    if url_input is None or url_input is '':
        url_input = 'https://www.afr-web.co.jp/hebel-rooms/search/detail/?clientcorp_room_cd=B201334160402'
    df = fill_dataframe_with_info(url_input)
    df = add_custom_headers(df)
    # Display DataFrame as table using streamlit
    st.write(df)
    generate_map(df)

# def extract_coordinates(df) -> Tuple[str,str]:
#     map_link = df.loc[0].at["Maps"]
#     longi = map_link[34:49]
#     lati = map_link[52:]
#     return (lati, longi)

def add_custom_headers(df:pd.DataFrame) -> pd.DataFrame:
    headers =  ["Name", "Link", "Address", "Maps", "Monthly price", "Surface (m2)", "Price/m2", "Age", "Type", "Shape", "Closest stations", "Amita Kanda", "MCP Otemachi", "Shinagawa", "XTIA", "Recursive Ebisu", "Ikebukuro", "Musashi Urawa", "Amita Kanda2", "MCP Otemachi2", "Shinagawa2", "XTIA2", "Recursive Ebisu2", "Ikebukuro2", "Musashi Urawa2"]
    df.columns = headers
    return df

def generate_map(df:pd.DataFrame):
    # TODO: add coordinates to DataFrame; add option to not display it
    # lati, longi = coordinates
    data = pd.DataFrame(
        {   'Name': [df.loc[0].at['Name']],
            'Link': [df.loc[0].at['Link']],
            'latitude': [float(df.loc[0].at["Maps"][34:49])],
            'longitude': [float(df.loc[0].at["Maps"][52:])]
        })
    st.map(data = data)
    # Add icon to all objects
    # icon_data = {
    #     "url": ICON_URL,
    #     "width": 242,
    #     "height": 242,
    #     "anchorY": 242,
    # }
    # data["icon_data"] = None
    # for i in data.index:
    #     data["icon_data"][i] = icon_data

    # longi = float(df.loc[0].at["Maps"][34:49])
    # lati = float(df.loc[0].at["Maps"][52:])
    # # view_state = pdk.data_utils.compute_view(data[["longitude", "latitude"]], 0.1)
    # # view_state = pdk.ViewState(longitude=longi, latitude=lati)

    # icon_layer = pdk.Layer(
    #     type="IconLayer",
    #     data=data,
    #     get_icon="icon_data",
    #     get_size=4,
    #     size_scale=15,
    #     pickable=True,
    # )

    # r = pdk.Deck(layers=[icon_layer], api_keys=MAPBOX_API_KEY, map_provider='mapbox', tooltip={"text": "{Name}"})

    # st.pydeck_chart(
    #         r
    #    )


if __name__ == '__main__':
    # df = fill_sheet_with_info('https://www.afr-web.co.jp/hebel-rooms/search/detail/?clientcorp_room_cd=B201334160402')
    generate_gui()