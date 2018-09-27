# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 00:58:35 2018

@author: Anubhav
"""
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pprint
import sys

ACCESS_TOKEN = "2809971486-5mKvKePcThcQ2kzeoZmNo7AXBTbDfvkszjzLhDN"
ACCESS_TOKEN_SECRET = "bW86Z7h2L4hun3NPiqQhkbWT3ElP4eTXrX0Q8BvxuWiSC"
CONSUMER_KEY = "pj7DbLI2behFKsIsAMJ21DBgR"
CONSUMER_SECRET = "ZleGkjuNzHZIEhKNUFuKtuDqbXPI0ixvXWsH6msVwrtX4SoC5e"

################# Twitter Client ##############

class TwitterClient():
    
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user


    def get_user_timeline_tweets(self,num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id = self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return str(tweets)

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id = self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return str(friend_list)

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id = self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return str(home_timeline_tweets)


            
################# Twitter Authenticator ########

class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return auth

################# Twitter Streamer #########
class TwitterStreamer():
    """
    class for streaming and processing tweets.
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()
    
    def stream_tweets(self, fetched_tweets_filename, hashtag_list):
        #Twiiter Authentication and connection with API
        listener = Twitterlistener(fetched_tweets_filename)
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        
        stream = Stream(auth, listener)
        stream.filter(track=hashtag_list)

class Twitterlistener(StreamListener):
    
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
    
    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data: {}".format(e))
        return True
    
    def on_error(self, status):
        if status == 420:
            # Return False on_data method
            return False
        print(status)
        
if __name__ == "__main__":
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    hashtag = ['Python','Ruby','JavaScript']
    fetched_tweets_filename = "tweets.txt"

    twitter_client = TwitterClient('Pycon')
    print(twitter_client.get_user_timeline_tweets(1).translate(non_bmp_map))
    print(twitter_client.get_friend_list(5).translate(non_bmp_map))
    print(twitter_client.get_home_timeline_tweets(2).translate(non_bmp_map))
    
    #twitter_streamer = TwitterStreamer()
    #twitter_streamer.stream_tweets(fetched_tweets_filename, hashtag)
