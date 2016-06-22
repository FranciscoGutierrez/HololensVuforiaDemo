from pattern.en import sentiment, polarity, subjectivity, positive
from TwitterAPI import TwitterAPI
from pymongo import MongoClient
import datetime
import json
import urllib2
import threading
from lxml import html
import requests

TRACK_TERM = 'Atlanta'
TRACK_LOC   = '-84.551819,33.647808,-84.289389,33.887618'

CONSUMER_KEY = 'b3HjgCfSrcsFAiBvHbHC617tm'
CONSUMER_SECRET = 'hHj9J3hIIaX03EJkDp2uJzOurt5TYg6J7ylNa1mApKnAa6Oqxr'
ACCESS_TOKEN_KEY = '19495636-tfJxdvlum1DWnGez1jBnZtpqqZQRyRbvsMdMpDAQt'
ACCESS_TOKEN_SECRET = '6ULLaZQLpyjifK6tDmAoGjBcpNmR2yro5kLEScW3JS5PS'

api = TwitterAPI(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN_KEY,ACCESS_TOKEN_SECRET)
r = api.request('statuses/filter', {'track': TRACK_TERM,'locations': TRACK_LOC})

client = MongoClient("mongodb://127.0.0.1:3001/meteor")
db = client['meteor']

for item in r.get_iterator():
    if 'text' in item:
        a = item['text']
        p = polarity(a)
        s = subjectivity(a)
        if (p != 0.0):
            post = {"track": "atlanta", "tweet": a, "tweetdate": datetime.datetime.utcnow(), "polarity": p, "subjectivity":s}
            db.tweets_denver.insert_one(post).inserted_id
            print("Denver")
