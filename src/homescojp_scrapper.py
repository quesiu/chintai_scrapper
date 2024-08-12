import re
from typing import Tuple
import json
from bs4 import BeautifulSoup as bs

from bukken import Bukken
from realestate_scrapper import RealEstateScrapper

# Regex to catch latitude and longitude for Homes
LAT_LONG_REGEX = r'{\"lat\":\"(\d*\.\d*)\",\"lng\":\"(\d*.\d*)\"}'
PRICE_REGEX = r'<span>(\d+\.?\d*)</span>.+\( (\d+,\d+)'
#EXTRA_FEES_REGEX = r'(\d.?\d?|-)(?:ヶ月)? / (.?\d?|-)(?:ヶ月)?'
EXTRA_FEES_REGEX = r'((?:[0-9]*[.])?[0-9]+|-)(?:ヶ月)?/((?:[0-9]*[.])?[0-9]+|-)(?:ヶ月)?'
MADORI_REGEX = r'(\d[SLDK]+)'
SURFACE_REGEX = r'(\d+\.?\d*)'

class HomescoojpScrapper(RealEstateScrapper):
    def __init__(self, url: str):
        """Constructor for Homes.co.jp scrapper

        Args:
            url (str): url to the homes.co.jp page to be scrapped
        """
        super().__init__(url)
        self.soup = bs(self.return_content(), features='html.parser')

    def scrap_coordinates(self) -> Tuple[str, str]:
        """Get coordinates from Homes.co.jp page

        Returns:
            Tuple[str, str]: latitude and longitude in this order
        """
        # TODO: confirm if comment below is fully outdated or not with more data, then remove/update
        lati = ''
        longi = ''
        #coordinates_raw = self.soup.find_all(id = 'contents')
        #coordinates_res = re.search(LAT_LONG_REGEX, str(coordinates_raw))
        coordinates_element = self.soup.find(attrs={"data-detail--map-surround-article-position-value": True})
        coordinates_data = json.loads(coordinates_element['data-detail--map-surround-article-position-value'])

        if coordinates_data:
            lati = float(coordinates_data['lat'])
            longi = float(coordinates_data['lng'])
        return (lati, longi)

    def scrap_name(self) -> str:
        """Get name from Homes.co.jp page

        Returns:
            str: name of the property_bukken
        """
        # TODO: confirm if comment below is fully outdated or not with more data, then remove/update
        name = ''
        #name_raw = self.soup.find(class_ = 'bukkenName')
        name = self.soup.find('span', class_='block text-sm detail-main-screen:text-base font-bold mt-1').text.strip()
        #if name_raw is not None:
        #    name = name_raw
        return name

    def scrap_price(self) -> Tuple[int, int]:
        """Get price from Homes.co.jp page

        Returns:
            Tuple[int, int]: price in JPY, with monthly rent and monthly fees in this order
        """
        # TODO: confirm if comment below is fully outdated or not with more data, then remove/update
        monthly_price = ''
        monthly_fees = ''
        #price_raw = self.soup.find(id = 'chk-bkc-moneyroom')
        #price_res = re.search(PRICE_REGEX, str(price_raw))
        #if price_res:
        
        # Cast into int and convert 1万 to 10000JPY
        monthly_price_raw = self.soup.find('span', class_='text-xl detail-main-screen:text-2xl').text.strip()
        #monthly_price_raw= monthly_text_element.find_next_sibling('dd').text.strip()
        monthly_price = int(''.join(filter(str.isdigit, monthly_price_raw))) * 10000

        #monthly_price = int(float(price_res.group(1)) * 10000)
        
        # Replace comma used as separator for monthly fees, cast into int
        monthly_fees_raw = self.soup.find('span', class_='text-base').text.strip()
        monthly_fees = int(monthly_fees_raw.replace(',', ''))
        return monthly_price, monthly_fees

    def scrap_other_fees(self) -> float:
        """Get fees such as reikin, shikin, etc. and sum them up

        Returns:
            float: extra fees in months
        """
        # TODO: confirm if comment below is fully outdated or not with more data, then remove/update
        total = 0
        # Start with reikin and shikikin
        reikin_text_element = self.soup.find('dt', text="敷金/礼金")
        reikin_raw = reikin_text_element.find_next_sibling('dd').text.strip()
        #reikin_raw = self.soup.find(id= 'chk-bkc-moneyshikirei')
        reikin_res = re.search(EXTRA_FEES_REGEX, str(reikin_raw))
        if reikin_res:
            # Replace potential - by 0 and cast to int
            reikin = float(reikin_res.group(1).replace('-', '0').replace('無', '0'))
            shikikin = float(reikin_res.group(2).replace('-', '0').replace('無', '0'))
            total = reikin + shikikin
        # Continue with hosho and other fees
        #hosho_raw = self.soup.find(id= 'chk-bkc-moneyhoshoukyaku')
        hosho_text_element = self.soup.find('dt', text="保証金/敷引・償却金")
        hosho_raw = hosho_text_element.find_next_sibling('dd').text.strip()
        hosho_res = re.search(EXTRA_FEES_REGEX, str(hosho_raw))
        if hosho_res:
            # Replace potential - by 0 and cast to int
            total += float(hosho_res.group(1).replace('-', '0')) + float(hosho_res.group(2).replace('-', '0'))

        return total

    def scrap_closest_stations(self) -> str:
        """Get closest stations

        Returns:
            str: stations listed with line return as separator
        """
        # TODO: confirm if comment below is fully outdated or not with more data, then remove/update
        stations = ''
        stations_text_element = self.soup.find('dt', text="交通")
        stations_raw = stations_text_element.find_next_sibling('dd')
        #stations_raw = self.soup.find(id= 'chk-bkc-fulltraffic')
        if stations_raw is not None:
            stations_list = stations_raw.find_all("p")
            for idx, station in enumerate(stations_list):
                # Add a line return character
                stations += f'{station.text}\n'
                if idx == 2:
                    stations = stations[:-1]
                    break
        return stations
    
    def scrap_bukken_type(self) -> str:
        """Get bukken type

        Returns:
            str: type in Japanese
        """
        # TODO: confirm if comment below is fully outdated or not with more data, then remove/update
        bukken_type = ''
        bukken_type = self.soup.find('span', class_='inline-block bg-mono-50 text-xs/none py-1 px-2 rounded-full').text.strip()
        #bukken_raw = self.soup.find(id='chk-bkh-type')
        #if bukken_raw is not None:
        #    bukken_type = bukken_raw.text
        return bukken_type

    def scrap_madori(self) -> str:
        """Get bukken shape (1DK, 3LDK, etc.) which is called madori

        Returns:
            str: shape
        """
        # TODO: confirm if comment below is fully outdated or not with more data, then remove/update
        madori = ''
        madori_text_element = self.soup.find('dt', text="間取り")
        madori_raw = madori_text_element.find_next_sibling('dd').text.strip()
        #madori_raw = self.soup.find(id='chk-bkc-marodi')
        if madori_raw is not None:
            madori_res = re.search(MADORI_REGEX, str(madori_raw))
            if madori_res is not None:
                madori = madori_res.group(1)
        return madori

    def scrap_surface(self) -> float:
        """Get surface

        Returns:
            float: surface in m2
        """
        # TODO: confirm if comment below is fully outdated or not with more data, then remove/update
        surface = 0
        #surface_raw = self.soup.find(id='chk-bkc-housearea')
        surface_text_element = self.soup.find('dt', text="専有面積")
        surface_raw = surface_text_element.find_next_sibling('dd').text.strip()
        if surface_raw is not None:
            surface_res = re.search(SURFACE_REGEX, str(surface_raw))
            surface = float(surface_res.group(1))
        return surface

    def scrap_age(self) -> str:
        """Get bukken age

        Returns:
            str: age in Japanese
        """
        # TODO: confirm if comment below is fully outdated or not with more data, then remove/update
        age = ''
        #age_raw = self.soup.find(id='chk-bkc-kenchikudate')
        age_text_element = self.soup.find('dt', text="築年月")
        age = age_text_element.find_next_sibling('dd').text.strip()
        #if age_raw is not None:
        #    age = age_raw.text
        return age

if __name__ == "__main__":
    scrapper = HomescoojpScrapper('https://www.homes.co.jp/chintai/room/ab65b75a46ee5ce06aa4a9d7f048adbe7fc2def3/')
    my_bukken = Bukken()
    scrapper.scrap_all(my_bukken)
    print(my_bukken)