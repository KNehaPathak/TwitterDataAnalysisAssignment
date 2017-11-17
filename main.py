import tweepy
import progressbar
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
from progressbar import ProgressBar, Percentage, Bar
import json
import sys


#Twitter app information
consumerKey = 'XXXXXXX'
consumerSecret = 'XXXXXX'
accessToken =  'XXXXXX'
accessSecret =  'XXXXXX'


max_tweets=10000

class FetchTweets(StreamListener):
    def __init__(self, api=None):
        self.num_tweets = 0
        self.pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=max_tweets).start()


    def on_data(self, data):
        with open('tweets_data.txt', 'a') as tweet_file:
            tweet_file.write(data)
            # Increment the number of tweets
            self.num_tweets += 1
            if self.num_tweets >= max_tweets:
                self.pbar.finish()
                sys.exit(0)
            else:
                self.pbar.update(self.num_tweets)
        return True
    def on_error(self, status):
        print(status)


#Get the OAuth token
auth = OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessSecret)
twitterStream = Stream(auth, FetchTweets())
#twitterStream.filter(track=keyword_list, languages=['en'])
twitterStream.filter(locations=[-180,-90,180,90], languages=['en'])
#twitterStream.sample()
