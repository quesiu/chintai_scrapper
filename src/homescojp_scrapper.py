import re
from typing import Tuple
from base_scrapper import BaseScrapper
from bs4 import BeautifulSoup as bs

# Regex to catch latitude and longitude for Homes
LAT_LONG_REGEX = r'{\"lat\":\"(\d*.\d*)\",\"lng\":\"(\d*.\d*)\"}'

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

    def scrap_price(self) -> Tuple[str, str]:
        """Get price from Homes.co.jp page

        Returns:
            str: price in 万円, with monthly rent and monthly fees in this order
        """

    def scrap_other_fees(self) -> Tuple[str, str]:
        """Get reikin and shikikin

        Returns:
            Tuple[str, str]: reikin and shikikin, in 万円
        """

    def scrap_closest_stations(self) -> str:
        """Get closest stations

        Returns:
            str: stations listed with line return as separator
        """
        

        

    # def save_as_html(self):
    #     with open("output1.html", "w") as file:
    #         file.write(str(self.return_text()))

    # def read_html(self, name="output1.html"):
    #     with open("output1.html", "r") as file:
    #         return bs(file.read(), features="html.parser")


if __name__ == "__main__":
    scrapper = HomescoojpScrapper('https://www.homes.co.jp/chintai/b-1438180002881/')
    # scrapper.save_as_html()
    # text = scrapper.read_html()
    scrapper.scrap_coordinates()
    scrapper.scrap_name()