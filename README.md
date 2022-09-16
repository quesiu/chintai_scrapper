# Chintai Scrapper

A script to automatically extract information from different online rental property pages in Japan and output a .csv file with everything.

## Pre-requisites

- Python
- [Google API Key](https://cloud.google.com/docs/authentication/api-keys)


## Installation

- Clone the repo
- Create a new virtual environment and activate it
```bash
python -m venv env_scrapper
source env_scrapper/bin/activate # Unix
env_scrapper/scripts/activate # Windows
```
- Install submodules
```bash
pip install -r requirements.txt
```
## Usage

1. In *sheets_handler.py*, change SPREADSHEET_ID (included in link of GoogleSpreadsheet), INPUT_SHEET_RANGE_NAME (Sheet name and row/columns) and OUTPUT_SHEET_RANGE_NAME depending on needs.
2. Change *dict_directions* or add elements by using Google Maps and right clicking on interest points and choosing the coordinates. Paste them in the list.
3. Change Priority to Fast, Cheap or Convenient in *main.py*.
4. Run *main.py*
5. Alternatively, copy a listing URL and paste it in *main_one_link.py* and run the file to get only one output.

## Known bugs

- Some Suumo listing might not work.
- There is supposed to be time within the URL to force time around 9am on a Monday in order to avoid issues with no results at night, etc., but unsure if really working.
