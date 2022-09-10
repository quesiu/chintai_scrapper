import re
from typing import Tuple
import requests
from bs4 import BeautifulSoup as bs

from bukken import Bukken
from realestate_scrapper import RealEstateScrapper

# Header used to simulate request from browser and avoid robot blockers
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# Regex to catch latitude and longitude for Homes
LAT_LONG_REGEX = r'{\"lat\":\"(\d*\.\d*)\",\"lng\":\"(\d*.\d*)\"}'
PRICE_REGEX = r'    '
EXTRA_FEES_REGEX = r'(\d.?\d?|-)(?:ヶ月)? / (.?\d?|-)(?:ヶ月)?'
MADORI_REGEX = r'(\d[SLDK]+)'
SURFACE_REGEX = r'(\d+\.?\d*)'
class SuumoScrapper(RealEstateScrapper):

    def __init__(self, url: str):
        super().__init__(url)
        self.soup = bs(self.return_content(), features='html.parser')
        # Need to access another page with map info to get coordinates
        # Hence add slash and kankyo/ to parse this other page
        url = self.add_slash_url(url)
        page_map = requests.get(f'{url}kankyo/', allow_redirects=False, headers=HEADERS)
        self.map_soup = bs(page_map.content, features='html.parser')

    def add_slash_url(self, url: str) -> str:
        # TODO: Move to tool library
        """Check if URL finished with a slash and add it if not

        Args:
            url (str): url to check

        Returns:
            str: url with slash as last character
        """
        if url.endswith('/'):
            return url
        else:
            return url+'/'

    def scrap_coordinates(self) -> Tuple[str, str]:
        """Get coordinates from Suumo kankyo page

        Returns:
            Tuple[str, str]: latitude and longitude in this order
        """
        lati = re.search(r'"lat": (\d+.\d+)', str(self.map_soup)).group(1)
        longi = re.search(r'"lng": (\d+.\d+)', str(self.map_soup)).group(1)
        return (lati, longi)

    def scrap_name(self) -> str:
        """Get name from Suumo page

        Returns:
            str: name of the header
        """
        name_raw = self.soup.find(class_ = 'section_h1-header-title')
        # Remove potential leading or trailing whitespaces
        return name_raw.text.lstrip('\r\n\t\t\t').rstrip('                        ')

    def scrap_price(self) -> Tuple[int, int]:
        """Get price from Homes.co.jp page

        Returns:
            Tuple[int, int]: price in JPY, with monthly rent and monthly fees in this order
        """
        monthly_price_raw = self.soup.find('div', class_= 'property_view_main-emphasis')
        if monthly_price_raw is None:
            # Backup check for span instead of div
            monthly_price_raw = self.soup.find('span', class_= 'property_view_note-emphasis')
        # Remove useless chracters
        monthly_price = monthly_price_raw.text.lstrip('\r\n\t\t\t\t\t\t\t\t\t\t').rstrip('万円')
        # Cast into int and convert 1万 to 10000JPY
        monthly_price = int(float(monthly_price) * 10000)
        # All in one line for monthly fees
        # TODO clean it up, add intermediate function to separate both
        monthly_fees_raw = self.soup.find('div', class_='property_data-body')
        monthly_fees = int(monthly_fees_raw.text.rstrip('万円').replace('-', '0'))
        return monthly_price, monthly_fees

    def scrap_other_fees(self) -> float:
        """Get fees such as reikin, shikin, etc. and sum them up

        Returns:
            float: extra fees in months
        """
        reikin_shikikin_raw = self.soup.find_all('div', class_='property_data-body')[1].text
        other_fees_raw = self.soup.find_all('div', class_='property_data-body')[2].text
        other_fees_raw = self.soup.find_all('div', class_='property_data-body')[3].text
        print(1)
        return 1

    def scrap_closest_stations(self) -> str:
        stations = ''
        soup_of_stations = self.soup.find_all('div', class_='property_view_detail-body')[2]
        stations_raw = soup_of_stations.find_all('div', class_='property_view_detail-text')
        for station in stations_raw:
            stations += f'{station.text}\n'
        # Remove last line return
        stations = stations[:-1]
        return stations

    def scrap_bukken_type(self) -> str:
        return self.soup.find_all('div', class_='property_data-body')[7].text.lstrip('\r\n\t\t\t\t\t\t\t\t\t\t\t')

    def scrap_madori(self) -> str:
        return self.soup.find_all('div', class_='property_data-body')[4].text.lstrip('\r\n\t\t\t\t\t\t\t\t\t\t\t')

    def scrap_surface(self) -> float:
        return self.soup.find_all('div', class_='property_data-body')[5].text.lstrip('\r\n\t\t\t\t\t\t\t\t\t\t\t')
    
    def scrap_age(self) -> str:
        return self.soup.find_all('div', class_='property_data-body')[8].text.lstrip('\r\n\t\t\t\t\t\t\t\t\t\t\t')

if __name__ == '__main__':
    sc = SuumoScrapper('https://suumo.jp/chintai/bc_100296177140/')
    # sc = SuumoScrapper('https://suumo.jp/chintai/jnc_000027743441/?bc=100292549920')
    # sc.add_slash_url()
    print(sc.scrap_closest_stations())