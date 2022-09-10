from typing import Tuple
from bukken import Bukken
from base_scrapper import BaseScrapper
from abc import ABC, abstractmethod


class RealEstateScrapper(ABC, BaseScrapper):
    def __init__(self, url: str):
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

    @abstractmethod
    def scrap_all(self, bukken:Bukken):
        pass