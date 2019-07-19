import sys
sys.path.append('../')
import listing
import ratings
import time
import defaults
import pymongo
import numpy as np

start_year = sys.argv[1]
end_year = sys.argv[2]
write_to_db = bool(sys.argv[3])

ratings_details = list()
titles = listing.get_listing(start_year, end_year)

for title_name in titles.keys():
    # print(title_name)
    title_id = titles[title_name].split('/')[-2]
    rating  = ratings.get_ratings(titles[title_name])
    # print rating
    if rating != None:
        bottom_rating = sum(rating['hist_percentage'][0:3])
        top_rating = sum(rating['hist_percentage'][7:10])
        middle_rating = sum(rating['hist_percentage'][3:7])
        if bottom_rating + top_rating > middle_rating:
            # print(bottom_rating, top_rating)
            rating['hist_polar'] = abs(bottom_rating - top_rating)
        else:
            rating['hist_polar'] = -1.0
        rating['name'] = title_name
        rating['_id'] = title_id
        ratings_details.append(rating)
    time.sleep(defaults.sleep)

# print ratings_details
polar = list()
for rating in ratings_details:
    polar.append(rating['hist_polar'])

indices = np.argsort(polar)

for i in indices:
    if polar[i] != -1.0:
        print(polar[i], ratings_details[i]['name'])

if write_to_db:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[defaults.db_name]
    mycol = mydb["ratings"]
    x = mycol.insert_many(ratings_details)
