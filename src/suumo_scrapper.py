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
PRICE_REGEX = r'<span>(\d+\.?\d*)</span>.+\( (\d+,\d+)'
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
        lati = re.search(r'"lat": (\d+.\d+)', str(self.map_soup)).group(1)
        longi = re.search(r'"lng": (\d+.\d+)', str(self.map_soup)).group(1)
        return (lati, longi)

    def scrap_name(self) -> str:
        return super().scrap_name()

    def scrap_price(self) -> Tuple[int, int]:
        return super().scrap_price()

    def scrap_other_fees(self) -> float:
        return super().scrap_other_fees()

    def scrap_closest_stations(self) -> str:
        return super().scrap_closest_stations()

    def scrap_bukken_type(self) -> str:
        return super().scrap_bukken_type()

    def scrap_madori(self) -> str:
        return super().scrap_madori()

    def scrap_surface(self) -> float:
        return super().scrap_surface()
    
    def scrap_age(self) -> str:
        return super().scrap_age()

if __name__ == '__main__':
    sc = SuumoScrapper('https://suumo.jp/chintai/bc_100296177140/')
    # sc.add_slash_url()
    sc.scrap_coordinates()
    print("oui")