import requests
from bs4 import BeautifulSoup
import sys

def rating_demographic(table):
    data = dict()
    rows = table.findAll('tr')[1:]
    ages = ["All Ages", "<18", "18-29", "30-44", "45+"]
    for row in rows:
        entries = row.findAll('td')
        key = entries[0].text.strip()
        data[key] = dict()
        i = 0
        for entry in entries[1:]:
            data[key][ages[i]] = dict()
            rating = entry.find('div', attrs={'class': 'bigcell'}).text.strip()
            if rating == "-":
                rating = 0.0
                votes = 0
            else:
                rating = float(rating)
                votes = int(entry.find('div', attrs={'class': 'smallcell'}).text.strip().replace(',', ''))
            data[key][ages[i]]["rating"] = rating
            data[key][ages[i]]["votes"] = votes
            i+=1
    # print data
    return data

def rating_other_demographic(table):
        data = dict()
        cols= table.findAll('tr')[0].findAll('th')
        header =  [col.text.strip() for col in cols]

        rows = table.findAll('tr')[1:]
        for row in rows:
            i = 0
            entries = row.findAll('td')
            for entry in entries:
                key = header[i]
                data[key] = dict()
                rating = entry.find('div', attrs={'class': 'bigcell'}).text.strip()
                if rating == "-":
                    rating = 0.0
                    votes = 0
                else:
                    rating = float(rating)
                    votes = int(entry.find('div', attrs={'class': 'smallcell'}).text.strip().replace(',', ''))

                data[key]["rating"] = rating
                data[key]["votes"] = votes
                i+=1
        # print data
        return data

def get_ratings(title_ref):
    relative_ref = title_ref
    base_url = "https://www.imdb.com"
    rating_url = base_url + relative_ref + "ratings"

    page = requests.get(rating_url)
    # print rating_url
    soup = BeautifulSoup(page.text, 'html.parser')
    # print soup
    ratings_available = soup.find('div', attrs={'class': 'title-ratings-sub-page'})\
        .find('div', attrs={'class' : 'sectionHeading'}).text.strip('\n').strip()

    # print ratings_available
    if ratings_available == "No Ratings Available":
        return None

    overall_ratings_table = soup.findAll('table')[0]
    overall_ratings = overall_ratings_table.findAll('tr')

    total_votes = 0
    histogram_votes = list()
    histogram_percentage = list()
    for rating in overall_ratings[1:]:
        cols = rating.findAll('td')
        stars = cols[0].text.strip('\n').strip()
        percentage = cols[1].text.strip('\n').strip().strip('%')
        number_of_votes = cols[2].text.strip('\n').strip().replace(',', '')
        total_votes += int(number_of_votes)
        # print stars, percentage, number_of_votes
        histogram_votes.append(int(number_of_votes))
        if percentage == "":
            percentage = "0.0"
        histogram_percentage.append(float(percentage))

    histogram_votes.reverse()
    histogram_percentage.reverse()

    ratings = rating_demographic( soup.findAll('table')[1])
    ratings.update(rating_other_demographic(soup.findAll('table')[2]))
    ratings['hist_votes'] = histogram_votes
    ratings['hist_percentage'] = histogram_percentage
    return ratings
    # print ratings
