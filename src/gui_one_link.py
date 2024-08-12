from typing import Tuple
import json
import io
import streamlit as st
import pandas as pd
import pydeck as pdk
from streamlit_option_menu import option_menu
from streamlit_folium import st_folium
import folium
# Custom libraries
from google_maps_handler import GoogleMapsHandler
from dataframe_handler import DataFrameHandler

# LAT_LONG_REGEX = r'{\"lat\":\"(\d*\.\d*)\",\"lng\":\"(\d*.\d*)\"}'
ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/0/01/Geokey.svg"

def fill_dataframe_with_info(urls:str) -> pd.DataFrame:
    # TODO: Refactor with Sheets Handler
    """Main function that initialize and run all scripts
    """
    # Initialize different objects
    gmh = GoogleMapsHandler()
    sh = DataFrameHandler()

    sh.initiate_df(urls)
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
    display_results('https://www.afr-web.co.jp/hebel-rooms/search/detail/?clientcorp_room_cd=B200400640101')
#     display_results(
#         '''https://suumo.jp/chintai/jnc_000076217981/
# https://suumo.jp/chintai/jnc_000050158310/''')

def generate_home():
    urls_input = st.text_area(label="Paste property URL page below", help="Add one or several links (one per line) and click on the button to analyze them")
    st.button("Analyze properties", on_click=display_results, args=[urls_input])

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

def display_results(urls_input:str):
    # print(f'{url_input} is of type {type(url_input)}')
    if urls_input is None:
        urls_input = 'https://www.afr-web.co.jp/hebel-rooms/search/detail/?clientcorp_room_cd=B201334160402'
    df = fill_dataframe_with_info(urls_input)
    
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
    # TODO: add coordinates to DataFrame; add option to stot display it
    # lati, longi = coordinates
    data = pd.DataFrame()
    data['Name'] = df['Name']
    data['Link'] = df['Link']
    # Extract coordinates by only taking relevant characters from GoogleMaps link
    data['latitude'] = df['Maps'].apply(lambda x:float(x[34:49]))
    data['longitude'] = df['Maps'].apply(lambda x:float(x[52:]))

    # m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=15)
    # for i, row in data.iterrows():
    #     folium.Marker(location=[row['latitude'], row['longitude']], popup=f"<a href={row['Link']}>{row['Name']}</a>").add_to(m)

    # st_folium(m)
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

    
    # # view_state = pdk.data_utils.compute_view(data[["longitude", "latitude"]], 0.1)
    # # view_state = pdk.ViewState(longitude=longi, latitude=lati)

    # icon_layer = pdk.Layer(
    #     type="IconLayer",
    #     data=data,
    #     get_icon="icon_data",
    #     get_size=4,
    #     size_scale=15,
    #     get_position=["longitude", "latitude"],
    #     pickable=True,
    # )

    # pdk.Deck(layers=[icon_layer], tooltip={"text": "{Name}"})
    # pdk.Deck(layers=[icon_layer], api_keys=MAPBOX_API_KEY, map_provider='mapbox', tooltip={"text": "{Name}"})

    # st.pydeck_chart(
    #         r
    #    )


if __name__ == '__main__':
    # df = fill_sheet_with_info('https://www.afr-web.co.jp/hebel-rooms/search/detail/?clientcorp_room_cd=B201334160402')
    generate_gui()