import requests
from bs4 import BeautifulSoup

url = "https://www.imdb.com/chart/top"
headers = {"accept-language": "en-US,en;q=0.9", "cache-control": "max-age=0", 'Cache-Control': 'no-cache'}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')

movie_listing = soup.find('tbody', attrs={'class': "lister-list"})

movies = movie_listing.findAll('tr')
for movie in movies:
    title = movie.find('td', attrs={'class': "titleColumn"}).find('a').text
    year = movie.find('td', attrs={'class': "titleColumn"}).find('span').text.strip(')').strip('(')
    rating = movie.find('td', attrs={'class': "imdbRating"}).text.strip('\n')
    full_ref = movie.find('td', attrs={'class': "titleColumn"}).find('a').attrs['href']
    relative_ref = full_ref.split(' ')[0]

    print title, year,rating
    print relative_ref
# print page.headers
