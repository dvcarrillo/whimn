##############################################################################
# David Vargas Carrillo - October 2017
# github.com/dvcarrillo
# File: tweet.py
# Script that tweets an image taken by the camera each time that someone
# mentions the specified Twitter account
##############################################################################

import tweepy
import datetime
import time

# Log in to Twitter
auth = tweepy.OAuthHandler('consumer_key',
    'consumer_secret')
auth.set_access_token('access_key',
    'access_secret')

# Get the API variable
api = tweepy.API(auth)

# Get the current time
actual_time = datetime.datetime.utcnow()
print 'Actual UTC time is ' + str(actual_time)

while True:
    time.sleep(10)
    # Get the last mention and its time and ID
    mentions = api.mentions_timeline(count=1)
    mention_user = mentions[0].user.screen_name
    mention_time = mentions[0].created_at
    mention_id = mentions[0].id

    # If the account is mentioned after the script is launched, it sends a tweet
    if mention_time >= actual_time:
        text = '@' + str(mention_user) + ' Cats make people happy!'
        new_status = api.update_with_media("./random_cat.jpeg", text, in_reply_to_status_id = mention_id)
        actual_time = datetime.datetime.utcnow()
        print 'A new tweet has been sent!'
    else:
        print 'Nothing new after 10s'
