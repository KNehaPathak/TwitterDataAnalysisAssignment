import aylien_news_api
from aylien_news_api.rest import ApiException
from pprint import pprint
import json
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob



aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = 'XXXX'
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = 'XXXX'

api_instance = aylien_news_api.DefaultApi()

class TwitterClient(object):
    def __init__(self):
        consumerKey = 'XXXX'
        consumerSecret = 'XXXXX'
        accessToken = 'XXXXX-XXXX'
        accessSecret = 'XXXXXX'
        try:
            self.auth = OAuthHandler(consumerKey, consumerSecret)
            self.auth.set_access_token(accessToken, accessSecret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        tweets = []
        try:
            fetched_tweets = self.api.search(q=query, count=count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))

api = TwitterClient()
######Top Five Queries Hard Coded for now as the keywords are not being fetched corectly.
query_text = ["donald trump","rahul gandhi","narendra modi","apple","moto"]
posCounter = 0
negCounter = 0
neutralCounter = 0
news_pos = []
news_neg = []
news_neutral = []
queryNumber = 0

for query_data in query_text:
    print("For :",query_data,"**********************")
    data = query_data
    text = data
    language = ['en']
    since = 'NOW-10DAYS'
    until = 'NOW'
    try:
        api_response = api_instance.list_stories(text=text, language=language, published_at_start=since, published_at_end=until)
        story = api_response.stories
    except ApiException as e:
        print("Exception when calling DefaultApi->list_stories: %s\n" % e)

    #print("heres what News thinks about the topic")
    pnews = [data for data in story if data.sentiment.body.polarity == 'positive']
    #print("Positive News percentage: {} %".format(100 * len(pnews) / len(story)))

    nnews = [data for data in story if data.sentiment.body.polarity == 'negative']
    #print("Negative News percentage: {} %".format(100 * len(nnews) / len(story)))

    neutralnews = [data for data in story if data.sentiment.body.polarity == 'neutral']
    #print("Neutral News percentage: {} %".format(100 * len(neutralnews) / len(story)))



    #########What Twitter Thinks of the Topic
    #print("heres what twitter thinks about the topic")
    api = TwitterClient()
    tweets = api.get_tweets(query=data, count=200)
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    #print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))

    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    #print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))

    neutraltweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
    #print("Neutral News percentage: {} %".format(100 * len(neutraltweets) / len(tweets)))

    print(": News Precentage Positive: {} %".format(100 * len(pnews) / len(story)),
          "Twitter Percent Positive {} %".format(100 * len(ptweets) / len(tweets)))

    print(": News Precentage Negetive: {} %".format(100 * len(nnews) / len(story)),
          "Twitter Percent Negetive {} %".format(100 * len(ntweets) / len(tweets)))

    print(": News Precentage Neutral: {} %".format(100 * len(neutralnews) / len(story)),
          "Twitter Percent Negetive {} %".format(100 * len(neutraltweets) / len(tweets)))

