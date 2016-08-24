from pattern.en import sentiment, polarity, subjectivity, positive
from TwitterAPI import TwitterAPI
from pymongo import MongoClient
import datetime
import json
import urllib2
import threading
from lxml import html
import requests

TRACK_TERM = 'Seattle'
TRACK_LOC   = '-122.435908,47.495551,-122.235903,47.734145'

CONSUMER_KEY = '----'
CONSUMER_SECRET = '----'
ACCESS_TOKEN_KEY = '----'
ACCESS_TOKEN_SECRET = '---'

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
            post = {"track": "seattle", "tweet": a, "tweetdate": datetime.datetime.utcnow(), "polarity": p, "subjectivity":s}
            db.tweets_seattle.insert_one(post).inserted_id
            print("Seattle")
            #print(a)
