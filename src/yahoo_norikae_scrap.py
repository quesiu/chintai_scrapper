'''
https://atooshi-note.com/python-yahoo-trans-scraping/
現在時刻から直近の乗換案内を検索して、到着時間を表示する
Yahoo乗換から到着時間をスクレイピングで抽出している
'''
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs
import urllib.parse # URLエンコード、デコード
import re

NORIKAE_REGEX = r'(\d+)'
TIME_REGEX = r'.+着(.+)'

# Headers to avoid bot anti-spam
USER_AGENT = ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36')

def lookup_time_transfers(start_point:str, end_point:str, priority:int=0) -> str:
    
    #
    if priority < 0 or priority > 2:
        priority = 0

    # Encore Japanese characters
    startstaen = urllib.parse.quote(start_point) # encode
    endstaen = urllib.parse.quote(end_point) # encode

    # Create the request URL
    url0 = 'https://transit.yahoo.co.jp/search/result?from='
    url1 = '&flatlon=&to='
    url2 = f'&viacode=&viacode=&viacode=&shin=&ex=&hb=&al=&lb=&sr=&type=1&ws=3&s={priority}&ei=&fl=1&tl=3&expkind=1&ticket=ic&mtf=1&userpass=1&detour_id=&fromgid=&togid=&kw='
    url = url0 + startstaen + url1 + endstaen + url2 + endstaen

    # Make the request, using a header and get the answer
    req = Request(url)
    req.add_header(USER_AGENT[0], USER_AGENT[1])
    content = urlopen(req)
    html = content.read().decode('utf-8')

    # Parse result html
    soup = bs(html, 'html.parser')

    # Return useful information
    nb_transfers = get_nb_transfers(soup)
    total_time = get_total_time(soup)
    return f'{total_time} - {nb_transfers} '

def get_nb_transfers(soup) -> str:
    """Get number of transfers from parsed Yahoo Norikae Annai page

    Args:
        soup (BeautifulSoup): parsed data

    Returns:
        str: transfers as a string
    """
    transfers = soup.select_one("li.transfer").text
    transfers_res = re.search(NORIKAE_REGEX, transfers)
    return f'乗換:{int(transfers_res.group(1))}'

def get_total_time(soup) -> str:
    """Get total amount of time the commute takes from parsed Yahoo Norikae Annai page

    Args:
        soup (BeautifulSoup): parsed data

    Returns:
        str: total time as a string with extra info
    """
    time = soup.select("li.time")
    time_res = re.search(TIME_REGEX, time[2].text)
    return time_res.group(1)

