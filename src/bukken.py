from typing import List

class Bukken:
    def __init__(self) -> None:
        """Constructor for Bukken class: hold all information about a given property
        """
        self._name = ''
        self._monthly_price = int(0)
        self._monthly_mgt_fees = int(0)
        self._extra_fees_in_months = float(0)
        self._coordinates = ('', '')
        self._surface = float(0)
        self._closest_stations = ''
        self._bukken_type = ''
        self._madori = ''
        self._age = ''
        self._gmaps_link = ''
        self._address_jp = ''
        self._listing_link = ''

    def __str__(self) -> str:
        """Output object as a string

        Returns:
            str: only gives name and monthly price
        """
        return f'{self.name} - {self.monthly_price}'

    def extract(self) -> List:
        """Return a list of fully filled items which will be exported to csv/sheet

        Returns:
            List: all items containted inside the bukken object
        """
        return [self.name,
                self.listing_link,
                self.address_jp,
                self.gmaps_link,
                f'={self.monthly_price}*(24+4+{self.extra_fees_in_months})/24+{self.monthly_mgt_fees}',
                self.surface,
                '',
                self.age,
                self.bukken_type,
                self.madori,
                self.closest_stations]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def monthly_price(self):
        return self._monthly_price

    @monthly_price.setter
    def monthly_price(self, value):
        self._monthly_price = value
    
    @property
    def monthly_mgt_fees(self):
        return self._monthly_mgt_fees

    @monthly_mgt_fees.setter
    def monthly_mgt_fees(self, value):
        self._monthly_mgt_fees = value

    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, value):
        self._coordinates = value

    @property
    def extra_fees_in_months(self):
        return self._extra_fees_in_months

    @extra_fees_in_months.setter
    def extra_fees_in_months(self, value):
        self._extra_fees_in_months = value

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, value):
        self._surface = value
    
    @property
    def closest_stations(self):
        return self._closest_stations

    @closest_stations.setter
    def closest_stations(self, value):
        self._closest_stations = value

    @property
    def bukken_type(self):
        return self._bukken_type

    @bukken_type.setter
    def bukken_type(self, value):
        self._bukken_type = value

    @property
    def madori(self):
        return self._madori

    @madori.setter
    def madori(self, value):
        self._madori = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        self._age = value

    @property
    def gmaps_link(self):
        return self._gmaps_link

    @gmaps_link.setter
    def gmaps_link(self, value):
        self._gmaps_link = value

    @property
    def address_jp(self):
        return self._address_jp

    @address_jp.setter
    def address_jp(self, value):
        self._address_jp = value

    @property
    def listing_link(self):
        return self._listing_link

    @listing_link.setter
    def listing_link(self, value):
        self._listing_link = value