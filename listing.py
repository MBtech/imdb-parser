import requests
from bs4 import BeautifulSoup
import sys
from defaults import *

start = sys.argv[1]
end = sys.argv[2]

listing_url = "https://www.imdb.com/search/title/?"
start_index=1
total=0
params = {'title_type': type, 'release_date': start+","+end,
"languages": languages, 'view': 'simple', 'start': str(start_index)}


page = requests.get(listing_url, params=params)
soup = BeautifulSoup(page.text, 'html.parser')
items = soup.findAll('div', attrs={'class': 'lister-item'})
total = soup.find('div', attrs={'class': 'desc'}).find('span').text.split()[2].replace(',', '')
total = int(total)
print total

for item in items:
    name = item.find('span', attrs={'class': 'lister-item-header'}).find('a')
    link = item.find('span', attrs={'class': 'lister-item-header'}).find('a').attrs['href'].split()[0]
    # print name.text.strip().strip('\n'), link
