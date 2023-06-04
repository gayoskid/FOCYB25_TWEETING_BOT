import tweepy
from Credential import *

client = tweepy.Client(BEARER_TOKEN, API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def Check_auth_conn():
    try:
        api.verify_credentials()
        print("Twitter API authenticated successfully")
    except tweepy.TweepyException as error:
        print("Error during authentication:", str(error))
