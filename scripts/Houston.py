from pattern.en import sentiment, polarity, subjectivity, positive
from TwitterAPI import TwitterAPI
from pymongo import MongoClient
import datetime
import json
import urllib2
import threading
from lxml import html
import requests

TRACK_TERM = 'Houston'
TRACK_LOC   = '-95.788087,29.523624,-95.014496,30.110732'

CONSUMER_KEY = 'vp4vDnkSY5RiozYE7ljBuxSCN'
CONSUMER_SECRET = 'Wn1THfpm2H8Tc5ruG7b9NsJzA3C966XaKWMkrAQuk7q4PC4lgT'
ACCESS_TOKEN_KEY = '19495636-ijh8Wtv6MvSBXj4CsOx7LTIdECQ6cNeWlES7jFjO5'
ACCESS_TOKEN_SECRET = 'b163IxuQDj72zPAK0ec50lvMzMZ2bW2ZRBwm3oM28UeZr'

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
            post = {"track": "houston", "tweet": a, "tweetdate": datetime.datetime.utcnow(), "polarity": p, "subjectivity":s}
            db.tweets_houston.insert_one(post).inserted_id
            print("Houston")
            #print(a)
