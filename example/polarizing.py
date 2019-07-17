import sys
sys.path.append('../')
import listing
import ratings
import time
import defaults

start_year = sys.argv[1]
end_year = sys.argv[2]
ratings_details = dict()
titles = listing.get_listing(start_year, end_year)

for title_name in titles.keys():
    print(title_name)
    rating  = ratings.get_ratings(titles[title_name])
    print rating
    if rating != None:
        ratings_details[title_name] = rating
    time.sleep(defaults.sleep)

print ratings_details
