import os
import tweepy
from time import sleep
from dotenv import load_dotenv

# Loading environemnt variables (API keys, access tokens, etc.)
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_KEY_SECRET = os.getenv('API_KEY_SECRET')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Setup tweepy to twitter authentication
auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Variable declarions
FILE_NAME = "./last_tweet.txt"
HASHTAG = "#nsfwtwt"

tweetNumber = 100

def read_last_seen(FILE_NAME):
    file_read = open(FILE_NAME, 'r')
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id

def store_last_seen(FILE_NAME, last_seen_id):
    file_write = open(FILE_NAME, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    return

def reply():
    tweets = api.mentions_timeline(read_last_seen(FILE_NAME), tweet_mode='extended')
    for tweet in reversed(tweets):
        if HASHTAG in tweet.full_text.lower():
            print(str(tweet.id) + ' - ' + tweet.full_text)
            api.update_status("@" + tweet.user.screen_name + " Auto reply, like, and retweet works! :)", tweet.id)
            api.tetweet(tweet.id)
            store_last_seen(FILE_NAME, tweet.id)

def searchBot():
    tweets_finder = tweepy.Cursor(api.search, HASHTAG).items(tweetNumber)
    for tweet in tweets_finder:
        try:
            tweet.retweet()
            print("Retweet success!")
            sleep(2)
        except tweepy.TweepError as e:
            print(e.reason)
            sleep(2)


if __name__ =="__main__":
    while True:
        searchBot()
        print("Sleeping - 15 seconds..")
        sleep(15)