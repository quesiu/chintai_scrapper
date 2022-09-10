import googlemaps
from datetime import datetime
import yahoo_norikae_scrap as yns
from enum_priority import Priority

LANG_JP = 'ja'
LANG_EN = 'en'

def get_file_contents(filename:str) -> str:
    # TODO should be added to a tool library
    """Given a filename,
        return the contents of that file

    Args:
        filename (str): name of the file

    Returns:
        str: contents of the file
    """
    try:
        with open(filename, 'r') as f:
            # It's assumed our file contains a single line,
            # with our API key
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % filename)


if __name__ == '__main__':
    filename = 'gmaps_apikey'
    api_key = get_file_contents(filename)
    gmaps = googlemaps.Client(key=api_key)

    # address1 = gmaps.reverse_geocode('35.61057793782,139.72723070545', language=LANG_JP)[0]['formatted_address']
    # address2 = gmaps.reverse_geocode('35.69435423429964,139.77095724524028', language=LANG_JP)[0]['formatted_address']
    address1 = gmaps.reverse_geocode('35.897402237391475, 139.62741857125286', language=LANG_JP)[0]['formatted_address']
    address2 = gmaps.reverse_geocode('35.73165247913772, 139.72875962983719', language=LANG_JP)[0]['formatted_address']
    print(yns.lookup_time_transfers(address1, address2, priority=Priority.Convenient.value))