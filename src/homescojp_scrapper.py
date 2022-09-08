import re
from typing import Tuple
from base_scrapper import BaseScrapper
from bs4 import BeautifulSoup as bs

# Regex to catch latitude and longitude for Homes
LAT_LONG_REGEX = r'{\"lat\":\"(\d*\.\d*)\",\"lng\":\"(\d*.\d*)\"}'
PRICE_REGEX = r'<span>(\d+\.?\d*)</span>.+\( (\d+,\d+)'
EXTRA_FEES_REGEX = r'(\d.?\d?|-)(?:ヶ月)? / (.?\d?|-)(?:ヶ月)?'

class HomescoojpScrapper(BaseScrapper):
    def __init__(self, url: str):
        super().__init__(url)
        self.soup = bs(self.return_content(), features='html.parser')

    def scrap_coordinates(self) -> Tuple[str, str]:
        """Get coordinates from Homes.co.jp page

        Returns:
            Tuple[str, str]: latitude and longitude in this order
        """
        lati = ''
        longi = ''
        coordinates_raw = self.soup.find_all(id = 'contents')
        coordinates_res = re.search(LAT_LONG_REGEX, str(coordinates_raw))
        if coordinates_res:
            lati = coordinates_res.group(1)
            longi = coordinates_res.group(2) 
        return lati, longi

    def scrap_name(self) -> str:
        """Get name from Homes.co.jp page

        Returns:
            str: name of the property_bukken
        """
        name_raw = self.soup.find(class_ = 'bukkenName')
        return name_raw.text

    def scrap_price(self) -> Tuple[int, int]:
        """Get price from Homes.co.jp page

        Returns:
            Tuple[int, int]: price in JPY, with monthly rent and monthly fees in this order
        """
        monthly_price = ''
        monthly_fees = ''
        price_raw = self.soup.find(id = 'chk-bkc-moneyroom')
        price_res = re.search(PRICE_REGEX, str(price_raw))
        if price_res:
            # Cast into int and convert 1万 to 10000JPY
            monthly_price = int(price_res.group(1)) * 10000
            # Replace comma used as separator for monthly fees, cast into int
            monthly_fees = int(price_res.group(2).replace(',', ''))
        return monthly_price, monthly_fees

    def scrap_other_fees(self) -> float:
        """Get fees such as reikin, shikin, etc. and sum them up

        Returns:
            float: extra fees in months
        """
        total = 0
        # Start with reikin and shikikin
        reikin_raw = self.soup.find(id= 'chk-bkc-moneyshikirei')
        reikin_res = re.search(EXTRA_FEES_REGEX, str(reikin_raw))
        if reikin_res:
            # Replace potential - by 0 and cast to int
            total = int(reikin_res.group(1).replace('-', '0')) + int(reikin_res.group(2).replace('-', '0'))
        # Continue with hosho and other fees
        hosho_raw = self.soup.find(id= 'chk-bkc-moneyhoshoukyaku')
        hosho_res = re.search(EXTRA_FEES_REGEX, str(hosho_raw))
        if hosho_res:
            # Replace potential - by 0 and cast to int
            total += int(hosho_res.group(1).replace('-', '0')) + int(hosho_res.group(2).replace('-', '0'))

        return total

    def scrap_closest_stations(self) -> str:
        """Get closest stations

        Returns:
            str: stations listed with line return as separator
        """
    
    def scrap_bukken_type(self) -> str:
        """Get bukken type

        Returns:
            str: type in Japanese
        """

    def scrap_madori(self) -> str:
        """Get bukken shape (1DK, 3LDK, etc.) which is called madori

        Returns:
            str: shape
        """

    def scrap_surface(self) -> float:
        """Get surface

        Returns:
            float: surface in m2
        """

    def scrap_age(self) -> str:
        """Get bukken age

        Returns:
            str: age in Japanese
        """

if __name__ == "__main__":
    scrapper = HomescoojpScrapper('https://www.homes.co.jp/chintai/b-1438180002881/')
    scrapper.scrap_other_fees()