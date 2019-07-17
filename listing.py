import requests
from bs4 import BeautifulSoup
import sys
import defaults
import time

def get_listing_page(start_index, start_year, end_year):
    listing_url = "https://www.imdb.com/search/title/?"
    total=0
    params = {'title_type': defaults.type, 'release_date': start_year+","+end_year,
    "languages": defaults.languages, 'view': defaults.view, 'start': str(start_index)}


    page = requests.get(listing_url, params=params)
    soup = BeautifulSoup(page.text, 'html.parser')
    items = soup.findAll('div', attrs={'class': 'lister-item'})
    meta = soup.find('div', attrs={'class': 'desc'}).find('span').text.split()
    if len(meta) == 2:
        total = meta[0].replace(',', '')
    else:
        total = meta[2].replace(',', '')
    total = int(total)
    # print total

    titles = dict()
    for item in items:
        name = item.find('span', attrs={'class': 'lister-item-header'}).find('a').text
        link = item.find('span', attrs={'class': 'lister-item-header'}).find('a').attrs['href'].split()[0]
        titles[name] = link
    return total, titles


# start = sys.argv[1]
# end = sys.argv[2]
def get_listing(start_year, end_year):
    total = 50
    start_index = 1
    titles = dict()
    while start_index <= total:
        total, returned_titles = get_listing_page(start_index, start_year, end_year)
        titles.update(returned_titles)
        start_index += 50
        time.sleep(defaults.sleep)
    return titles
