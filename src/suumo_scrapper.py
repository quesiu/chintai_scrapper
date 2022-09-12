import re
import requests
from typing import Tuple
from bs4 import BeautifulSoup as bs

from bukken import Bukken
from google_maps_handler import GoogleMapsHandler
from realestate_scrapper import RealEstateScrapper

# Header used to simulate request from browser and avoid robot blockers
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# Regex to catch latitude and longitude for Homes
LAT__REGEX = r'"lat": (\d+.\d+)'
LONG_REGEX = r'"lng": (\d+.\d+)'
EXTRA_FEES_REGEX = r'(\d+.?\d*万円|-)'

class SuumoScrapper(RealEstateScrapper):
    # TODO: Add support for pages that have to be scrapped differently, see example in __main__
    def __init__(self, url: str):
        """Constructor for Suumo scrapper

        Args:
            url (str): url to the Suumo page to be scrapped
        """
        super().__init__(url)
        self.soup = bs(self.return_content(), features='html.parser')
        # Need to access another page with map info to get coordinates
        # Hence add slash and kankyo/ to parse this other page
        url = self.add_slash_url(url)
        page_map = requests.get(f'{url}kankyo/', allow_redirects=False, headers=HEADERS)
        self.map_soup = bs(page_map.content, features='html.parser')
        self.monthly_price = 0

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
        lati = ''
        longi = ''
        lati_res = re.search(LAT__REGEX, str(self.map_soup))
        longi_res = re.search(LONG_REGEX, str(self.map_soup))
        if lati_res is not None and longi_res is not None:
            lati = lati_res.group(1)
            longi = longi_res.group(1)
        else:
            lati, longi = self.fallback_coordinates()
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
        # Also add monthly price info to calculate extra fees in months
        self.monthly_price = monthly_price
        # All in one line for monthly fees
        # TODO clean it up, add intermediate function to separate both
        monthly_fees_raw = self.soup.find_all('div', class_='property_data-body')
        if len(monthly_fees_raw) > 0:
            monthly_fees_raw = monthly_fees_raw[0]
            monthly_fees = int(monthly_fees_raw.text.rstrip('万円').replace('-', '0'))
        else:
            monthly_fees = -1
        return monthly_price, monthly_fees

    def scrap_other_fees(self) -> float:
        # TODO refactor in a better way
        """Get fees such as reikin, shikin, etc. and sum them up

        Returns:
            float: extra fees in months
        """
        total_months = 0
        self.all_sub_info = self.soup.find_all('div', class_='property_data-body')
        if len(self.all_sub_info) > 1:
            reikin_shikikin_raw = self.all_sub_info[1].text
            reikin_shikinkin_res = re.search(EXTRA_FEES_REGEX, reikin_shikikin_raw)
            reikin = float(reikin_shikinkin_res.group(0).rstrip('万円').replace('-','0'))
            shikikin = float(reikin_shikinkin_res.group(1).rstrip('万円').replace('-','0'))
        else:
            reikin = -1
            shikikin = -1
        if len(self.all_sub_info) > 2:
            hoken_raw = self.all_sub_info[2].text
            hoken = float(hoken_raw.lstrip('\r\n\t\t\t\t\t\t\t\t\t\t\t\t').rstrip('万円').replace('-','0'))
        else:
            hoken = -1
        if len(self.all_sub_info) > 3:
            other_fees_raw = self.all_sub_info[3].text
            other_fees = float(other_fees_raw.lstrip('r\n\t\t\t\t\t\t\t\t\t\t\t\t').rstrip('万円').replace('-','0'))
        else:
            other_fees = -1
        total = reikin + shikikin + hoken + other_fees
        if self.monthly_price == 0:
            print("Error, monthly price not correctly output so not possible to calculate fees in months")
        else:
            # Convert in JPY and divide by monthly rent
            total_months = total * 10000 / self.monthly_price
        return total_months

    def scrap_closest_stations(self) -> str:
        """Get closest stations

        Returns:
            str: stations listed with line return as separator
        """
        stations = ''
        if len(self.all_sub_info) > 2:
            soup_of_stations = self.all_sub_info[2]
            stations_raw = soup_of_stations.find_all('div', class_='property_view_detail-text')
            for station in stations_raw:
                stations += f'{station.text}\n'
            # Remove last line return
            stations = stations[:-1]
        return stations

    def scrap_bukken_type(self) -> str:
        """Get bukken type

        Returns:
            str: type in Japanese
        """
        bukken_type = ''
        if len(self.all_sub_info) > 7:
            bukken_type = self.all_sub_info[7].text.lstrip('\r\n\t\t\t\t\t\t\t\t\t\t\t')
        return bukken_type

    def scrap_madori(self) -> str:
        """Get bukken shape (1DK, 3LDK, etc.) which is called madori

        Returns:
            str: shape
        """
        madori = ''
        if len(self.all_sub_info) > 4:
            madori = self.all_sub_info[4].text.lstrip('\r\n\t\t\t\t\t\t\t\t\t\t\t')
        return madori

    def scrap_surface(self) -> float:
        """Get surface

        Returns:
            float: surface in m2
        """
        surface = 0
        if len(self.all_sub_info) > 5:
            surface = self.all_sub_info[5].text.lstrip('\r\n\t\t\t\t\t\t\t\t\t\t\t').rstrip('m2')
        return float(surface)
    
    def scrap_age(self) -> str:
        age = ''
        if len(self.all_sub_info) > 8:
           age = self.all_sub_info[8].text.lstrip('\r\n\t\t\t\t\t\t\t\t\t\t\t')
        return age

    def fallback_coordinates(self) -> Tuple[str, str]:
        lati = ''
        longi = ''
        try:
            address_tag = self.soup.find(text='所在地').parent.parent
            lati = address_tag.find(class_="property_view_table-body").text
        except AttributeError:
            # No 所在地 element detected
            pass
        return (lati, longi)


if __name__ == '__main__':
    scrapper = SuumoScrapper('https://suumo.jp/chintai/bc_100296177140/')
    # sc = SuumoScrapper('https://suumo.jp/chintai/jnc_000027743441/?bc=100292549920') # Different scrapping needed
    my_bukken = Bukken()
    scrapper.scrap_all(my_bukken)
    print(my_bukken)