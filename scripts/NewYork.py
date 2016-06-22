from pattern.en import sentiment, polarity, subjectivity, positive
from TwitterAPI import TwitterAPI
from pymongo import MongoClient
import datetime
import json
import urllib2
import threading
from lxml import html
import requests

TRACK_TERM = 'New York'
TRACK_LOC  = '-74.255735,40.496044,-73.700272,40.915256'

CONSUMER_KEY = 'ffRDAmzSjDXaSvFAVWUhY6QxT'
CONSUMER_SECRET = 'mscDMGpg1wDQbQZ9VqHfKL8f7wQbUSUbZMGd0oD6sxy3vBeF84'
ACCESS_TOKEN_KEY = '19495636-lcYOEgKPfOp4xky5CTGQwzf5VdZuIcVV1ifGOi3ss'
ACCESS_TOKEN_SECRET = 'I4O0FciZA8HxqGgC6jEz6oS21kHWObPChLpI9Syd299Jf'

api = TwitterAPI(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN_KEY,ACCESS_TOKEN_SECRET)
r = api.request('statuses/filter', {'track': TRACK_TERM,'locations': TRACK_LOC})

### MongoDB Calling
client = MongoClient("mongodb://127.0.0.1:3001/meteor")
db = client['meteor']

for item in r.get_iterator():
    if 'text' in item:
        a = item['text']
        p = polarity(a)
        s = subjectivity(a)
        if (p != 0.0):
            post = {"track": "newyork", "tweet": a, "tweetdate": datetime.datetime.utcnow(), "polarity": p, "subjectivity":s}
            db.tweets_newyork.insert_one(post).inserted_id
            print("NewYork")
            #print(a)
