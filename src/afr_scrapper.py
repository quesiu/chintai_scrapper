import re
from typing import Tuple
from bs4 import BeautifulSoup as bs

from bukken import Bukken
# from google_maps_handler import GoogleMapsHandler
from realestate_scrapper import RealEstateScrapper

# Header used to simulate request from browser and avoid robot blockers
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# Regex to catch latitude and longitude for Homes
LAT_REGEX = r'var lat = (\d+.\d+)'
LONG_REGEX = r'var lon = (\d+.\d+)'
MONTHLY_FEES_REGEX = r'(\d+.\d*)'
EXTRA_FEES_REGEX = r'(\d+|-)'
MADORI_REGEX = r'\d[SLDK]+'

class AfrWebScrapper(RealEstateScrapper):
    def __init__(self, url: str):
        """Constructor for afr scrapper

        Args:
            url (str): url to the Suumo page to be scrapped
        """
        super().__init__(url)
        self.soup = bs(self.return_content(), features='html.parser')
    
    def scrap_coordinates(self) -> Tuple[str, str]:
        """Get coordinates from Suumo kankyo page

        Returns:
            Tuple[str, str]: latitude and longitude in this order
        """
        lati = ''
        longi = ''
        lati_res = re.search(LAT_REGEX, str(self.soup))
        longi_res = re.search(LONG_REGEX, str(self.soup))
        if lati_res is not None and longi_res is not None:
            lati = lati_res.group(1)
            longi = longi_res.group(1)
        return (lati, longi)

    def scrap_name(self) -> str:
        """Get name from Suumo page

        Returns:
            str: name of the header
        """
        name = ''
        name_raw = self.soup.find('span', class_ = 'property-page-tit-text')
        if name_raw is not None:
            name = name_raw.text
        return name

    def scrap_price(self) -> Tuple[int, int]:
        """Get price from afr page

        Returns:
            Tuple[int, int]: price in JPY, with monthly rent and monthly fees in this order
        """
        monthly_price = -1
        monthly_fees = -1
        monthly_price_and_fees_raw = self.soup.find('span', class_= 'detail-mainimg-infocolor')
        if monthly_price_and_fees_raw is not None:
            monthly_price_and_fees_res = re.findall(MONTHLY_FEES_REGEX, monthly_price_and_fees_raw.text)
            if len(monthly_price_and_fees_res) > 1:
                # Cast into int and convert 1万 to 10000JPY
                monthly_price = int(float(monthly_price_and_fees_res[0]) * 10000)
                monthly_fees = int(float(monthly_price_and_fees_res[1]) * 10000)
        return monthly_price, monthly_fees

    def scrap_other_fees(self) -> float:
        """Get fees such as reikin, shikin, etc. and sum them up

        Returns:
            float: extra fees in months
        """
        total_months = 0
        shikikin = -1
        reikin = -1
        # Get shikikin info
        shikikin_raw = self.soup.find('span', class_='detail-info-deposit')
        if shikikin_raw is not None:
            shikikin_res = re.findall(EXTRA_FEES_REGEX, shikikin_raw.text)
            if shikikin_res is not None:
                shikikin = int(shikikin_res[0].replace('-', '0'))
        # Get reikin info
        reikin_raw = self.soup.find('span', class_='detail-info-gratuityfee')
        if reikin_raw is not None:
            reikin_res = re.findall(EXTRA_FEES_REGEX, reikin_raw.text)
            if reikin_res is not None:
                reikin = int(reikin_res[0].replace('-', '0'))
        total_months = shikikin + reikin
        return total_months

    def scrap_closest_stations(self) -> str:
        """Get closest stations

        Returns:
            str: stations listed with line return as separator
        """
        stations = ''
        stations_raw = self.soup.find('p', class_='detail-info-accesstxt')
        if stations_raw is not None:
            stations = stations_raw.text
            # Add line return
            stations = stations.replace('分', '分\n')
            stations = stations.rstrip('\n')
        return stations

    def scrap_bukken_type(self) -> str:
        """Get bukken type

        Returns:
            str: type in Japanese
        """
        bukken_type = ''
        bukken_text = self.soup.find(text='物件種別')
        if bukken_text is not None:
            bukken_section = bukken_text.parent.parent
            bukken_type_raw = bukken_section.find('dd', class_='bukken-info-detail-dd')
            if bukken_type_raw is not None:
                bukken_type = bukken_type_raw.text
        return bukken_type

    def scrap_madori(self) -> str:
        """Get bukken shape (1DK, 3LDK, etc.) which is called madori

        Returns:
            str: shape
        """
        madori = ''
        madori_raw = self.soup.find('dd', class_='detail-mainimg-infolistdesc detail-mainimg-infolistfloor')
        if madori_raw is not None:
            madori_res = re.findall(MADORI_REGEX, madori_raw.text)
            if len(madori_res) > 0:
                madori = madori_res[0]
        return madori

    def scrap_surface(self) -> float:
        """Get surface

        Returns:
            float: surface in m2
        """
        surface = 0
        surface_raw = self.soup.find('span', class_='detail-mainimg-roomsize')
        if surface_raw is not None:
            surface = surface_raw.text.rstrip('m2')
        return float(surface)
    
    def scrap_age(self) -> str:
        age = ''
        age_raw = self.soup.find('dd', class_='detail-info-desc detail-info-desc-dt3text')
        if age_raw is not None:
            age = age_raw.text
        return age

if __name__ == '__main__':
    scrapper = AfrWebScrapper('https://www.afr-web.co.jp/hebel-rooms/search/detail/?clientcorp_room_cd=B20211920201')
    my_bukken = Bukken()
    scrapper.scrap_all(my_bukken)
    print(my_bukken)