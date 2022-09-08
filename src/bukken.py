class Bukken:
    def __init__(self) -> None:
        self._name = ''
        self._monthly_price = ''
        self._monthly_mgt_fees = ''
        self._reikin = ''
        self._shikikin = ''
        self._coordinates = ('', '')
        self._surface = ''
        self._closest_stations = ''

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
    def reikin(self):
        return self._reikin

    @reikin.setter
    def reikin(self, value):
        self._reikin = value

    @property
    def shikikin(self):
        return self._shikikin

    @shikikin.setter
    def shikikin(self, value):
        self._shikikin = value

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