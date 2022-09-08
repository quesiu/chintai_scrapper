import re
from base_scrapper import BaseScrapper
from bs4 import BeautifulSoup as bs

# Regex to catch latitude and longitude for Homes
LAT_LONG_REGEX = r'{\"lat\":\"(\d*.\d*)\",\"lng\":\"(\d*.\d*)\"}'

class ChintaiScrapper(BaseScrapper):
    def get_coordinates(self):
        lati, longi = 0, 0
        soup = bs(self.return_content(), features='html.parser')
        contents = soup.find_all(id = 'contents')
        results = re.search(LAT_LONG_REGEX, str(contents))
        if results:
            lati = results.group(1)
            longi = results.group(2)
        return (lati, longi)

    # def save_as_html(self):
    #     with open("output1.html", "w") as file:
    #         file.write(str(self.return_text()))

    # def read_html(self, name="output1.html"):
    #     with open("output1.html", "r") as file:
    #         return bs(file.read(), features="html.parser")


if __name__ == "__main__":
    scrapper = ChintaiScrapper('https://www.homes.co.jp/chintai/b-1438180002881/')
    # scrapper.save_as_html()
    # text = scrapper.read_html()
    scrapper.get_coordinates()