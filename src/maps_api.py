import googlemaps
from datetime import datetime

def get_file_contents(filename:str) -> str:
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

    address1 = gmaps.reverse_geocode('35.61057793782,139.72723070545')[0]['formatted_address']
    address2 = gmaps.reverse_geocode('35.69435423429964,139.77095724524028')[0]['formatted_address']
    print('test')

    now = datetime.now()
    directions_result = gmaps.directions(address1,
                                     address2,
                                     mode="walking")
    print('test')