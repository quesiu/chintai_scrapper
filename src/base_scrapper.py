from pathlib import Path
import shutil
import os
import requests
from urllib.parse import urlparse
from os.path import splitext, basename
from bs4 import BeautifulSoup as bs
# try:
#     from googlesearch import search
# except ImportError:
#     print("Error: no module named 'google' found")

# Header used to simulate request from browser and avoid robot blockers
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

class BaseScrapper:
    
    def __init__(self, url:str):
        self.url = url
        self.page = requests.get(url, allow_redirects=True, headers=HEADERS)
        self.extract_name_and_ext()

    def show_page(self):
        print(self.page.text)

    def return_text(self):
        return self.page.text

    def return_content(self):
        return self.page.content

    def extract_name_and_ext(self):
        # Get site name and file extension
        # Note: could be isolated in an utility class
        disassembled = urlparse(self.url)
        self.filename, self.ext = splitext(basename(disassembled.path))

    def create_folder(self, path:Path):
        # Create folder whether it already exists or not
        # Note: could be isolated in an utility class
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)


if __name__ == "__main__":
    scrapper = BaseScrapper('https://www.homes.co.jp/chintai/b-1438180002881/')
    scrapper.show_page()
