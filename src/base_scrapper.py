import os
import shutil
import requests
from pathlib import Path
from urllib.parse import urlparse
from os.path import splitext, basename

# Header used to simulate request from browser and avoid robot blockers
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

class BaseScrapper:
    
    def __init__(self, url:str):
        """Constructor for base scrapper class

        Args:
            url (str): url to the real estate property page to be scrapped
        """
        self.url = url
        self.page = requests.get(url, allow_redirects=True, headers=HEADERS)
        self.extract_name_and_ext()

    def show_page(self):
        """Display text in page
        """
        print(self.page.text)

    def return_text(self) -> str:
        """Return text in page

        Returns:
            str: text
        """
        return self.page.text

    def return_content(self) -> str:
        """Return content 

        Returns:
            str: content (to be scrapped)
        """
        return self.page.content

    def extract_name_and_ext(self):
        # TODO: to be isolated in an utility class
        """Get site name and file extension
        """
        disassembled = urlparse(self.url)
        self.filename, self.ext = splitext(basename(disassembled.path))

    def create_folder(self, path:Path):
        """ Create folder whether it already exists or not

        Args:
            path (Path): path to the folder to be created
        """
        # TODO: to be isolated in an utility class
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)


if __name__ == "__main__":
    scrapper = BaseScrapper('https://www.homes.co.jp/chintai/b-1438180002881/')
    scrapper.show_page()
