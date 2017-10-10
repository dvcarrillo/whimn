##############################################################################
# David Vargas Carrillo - October 2017
# github.com/dvcarrillo
# File: whimn.py
# Script that tweets an image taken by the camera each time that someone
# mentions the specified Twitter account
##############################################################################

import datetime
import time
import sys
import tweepy
from picamera import PiCamera

camera = PiCamera()

# Log in to Twitter
auth = tweepy.OAuthHandler('k2C650dTflbGY9t1jZK92R7vZ',
                           'HD5shobNUdPtAiBAQs6UbFUIHUCn7jLu18McxPnXonirirT5pJ')
auth.set_access_token('234523159-pwMVglBunmBDD1iggW1PXvxgTFIrcZewtbFNBMyt',
                      'ce1VvxwHqstINlsLzSPPBWOvSkzISLFmfc09u0k16Wd0Z')

# Get the API variable
api = tweepy.API(auth)
print '#WhatHappensInMyNeighborhood'

# Get the current time
actual_time = datetime.datetime.utcnow()
print 'Actual UTC time is ' + str(actual_time)

# Start hearing mentions
print '\nHearing mentions now...'
start_status = api.update_status('#whimn hearing mentions now...')

# Infinite loop that reads mentions every 10s
while True:
    try:
        # Wait 10s
        time.sleep(10)
        # Get the last mention
        mentions = api.mentions_timeline(count=1)
        mention_user = mentions[0].user.screen_name
        mention_time = mentions[0].created_at
        mention_id = mentions[0].id
        # If the account is mentioned after the script is launched, it sends a tweet
        if mention_time >= actual_time:
            # Capture the photo
            camera.start_preview()
            time.sleep(5)
            camera.capture('./image.jpg')
            camera.stop_preview()
            # Make the new tweet
            text = '@' + str(mention_user) + ' This is my neighborhood at '
            text += str(datetime.datetime.utcnow().time()) + ' (UTC time)'
            photo_status = api.update_with_media("./image.jpg", text, 
                in_reply_to_status_id = mention_id)
            actual_time = datetime.datetime.utcnow()
            print 'A new tweet has been sent! (' + str(datetime.datetime.utcnow()) +')'
        else:
            print 'Nothing new...'
    # If something goes wrong, warn it and stop the execution
    except:
        api.destroy_status(start_status.id)
        api.update_status('#whimn stopped')
        print '\nStopping...'
        sys.exit()
