import requests
from bs4 import BeautifulSoup
import sys

relative_ref = sys.argv[1]
base_url = "https://www.imdb.com"
rating_url = base_url + relative_ref + "ratings"

page = requests.get(rating_url)
soup = BeautifulSoup(page.text, 'html.parser')

overall_ratings_table = soup.findAll('table')[0]
overall_ratings = overall_ratings_table.findAll('tr')

total_votes = 0
for rating in overall_ratings[1:]:
    cols = rating.findAll('td')
    stars = cols[0].text.strip('\n').strip()
    percentage = cols[1].text.strip('\n').strip().strip('%')
    number_of_votes = cols[2].text.strip('\n').strip().replace(',', '')
    total_votes += int(number_of_votes)
    print stars, percentage, number_of_votes
