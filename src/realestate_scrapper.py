from abc import ABC, abstractmethod
from typing import Tuple
from bukken import Bukken
from base_scrapper import BaseScrapper

# Part of the URL used to add a point to a given place
GMAPS_URL = r'https://www.google.com/maps/place/'

class RealEstateScrapper(ABC, BaseScrapper):
    def __init__(self, url: str):
        """Constructor for abstract class RealEstateScrapper

        Args:
            url (str): url to the real estate prioperty page to be scrapped
        """
        super().__init__(url)

    @abstractmethod
    def scrap_coordinates(self) -> Tuple[str, str]:
        pass

    @abstractmethod
    def scrap_name(self) -> str:
        pass

    @abstractmethod
    def scrap_price(self) -> Tuple[int, int]:
        pass

    @abstractmethod
    def scrap_other_fees(self) -> float:
        pass

    @abstractmethod
    def scrap_closest_stations(self) -> str:
        pass

    @abstractmethod
    def scrap_bukken_type(self) -> str:
        pass

    @abstractmethod
    def scrap_madori(self) -> str:
        pass

    @abstractmethod
    def scrap_surface(self) -> float:
        pass

    @abstractmethod
    def scrap_age(self) -> str:
        pass

    def scrap_all(self, bukken:Bukken):
        """Fill up an bukken object with all scrapped

        Args:
            bukken (Bukken): empty bukken that will be filled (in place)
        """
        bukken.name = self.scrap_name()
        bukken.monthly_price, bukken.monthly_mgt_fees = self.scrap_price()
        bukken.extra_fees_in_months = self.scrap_other_fees()
        bukken.coordinates = self.scrap_coordinates()
        bukken.surface = self.scrap_surface()
        bukken.closest_stations = self.scrap_closest_stations()
        bukken.bukken_type = self.scrap_bukken_type()
        bukken.madori = self.scrap_madori()
        bukken.age = self.scrap_age()
        # Create a link to Google Maps using coordinates
        bukken.gmaps_link = f'{GMAPS_URL}{bukken.coordinates[0]}%20{bukken.coordinates[1]}'