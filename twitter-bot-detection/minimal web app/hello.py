import requests

from flask import render_template
from flask import request
from flask import Flask

from requests_oauthlib import OAuth1Session

import json

app = Flask(__name__)

consumer_api = "EwzPvfqGW1eNZobsQT8JDzIU9"
consumer_secret = "3O1NKl6vXevtdmThkWP6aJDtCglXaq8eTwSckU2O69i70pktd8"

access_token = "141097960-Z9INLUm3cnUyVGAFTDZWsBsACWNEdWkfK4XxN0fY"
access_secret = "n9k4oOIeBbfphV9q7Lf3ZR8QgoWpJq80zn2EdrnhwOIZg"

import pandas as pd

import pickle

@app.route("/")
def hello():
    return render_template('sample.html')


@app.route("/user", methods=['POST'])
def handle_user():
    if request.method ==  'POST':
        url = 0
        url = request.form.get('url', url)
        twitter = OAuth1Session(consumer_api,
                            client_secret=consumer_secret,
                            resource_owner_key=access_token,
                            resource_owner_secret=access_secret)
        r = twitter.get('https://api.twitter.com/1.1/users/show.json?screen_name='+url)
        d = json.loads(r.content.decode("utf-8"))

        gen_acc = pd.DataFrame.from_dict(d)

        if len(gen_acc) <= 1:
                return render_template('process.html', url=0, message='Could not get data from twitter API.')
                


        gen_acc = gen_acc[['statuses_count', 'followers_count', 'friends_count', 'favourites_count', 
         'listed_count', 'default_profile', 'geo_enabled', 'profile_use_background_image', 
         'protected', 'verified']]


        filename = 'finalized_model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))

        RF_predictions = loaded_model.predict(gen_acc)

        print(RF_predictions)

        RF_predictions = sum(RF_predictions)

        return render_template('process.html', url=RF_predictions, message='')

