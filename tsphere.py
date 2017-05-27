from tweepy import Stream, OAuthHandler, API
from tweepy.streaming import StreamListener
from textblob import TextBlob
import json
import requests
import codecs
from colorama import init, Fore
init()

class TwitterSphere(StreamListener):

    def __init__(self):
        self.name = 'TwitterSphere'
        self.version = '0.1'

        #Keys from Twitter Developer Console, in the order below in keys.txt
        with open('keys.txt', 'r') as kfile:
            keys = kfile.read().split('\n')
        self.ckey = keys[0]
        self.csecret = keys[1]
        self.atoken = keys[2]
        self.asecret = keys[3]
        
        self.auth = OAuthHandler(self.ckey, self.csecret)
        self.auth.set_access_token(self.atoken, self.asecret)
        self.api = API(self.auth)
        self.total_sent = 0

    def on_data(self, data):
        try:
            all_data = json.loads(data)
#            print(str(len(all_data)))
            username = all_data['user']['screen_name']
            tweet = all_data['text']
            tweet_s = TextBlob(tweet)
            self.total_sent = self.total_sent + tweet_s.sentiment.polarity

            print(repr(tweet.encode('utf-8')))
            if tweet_s.sentiment.polarity > 0: #green
                print(Fore.GREEN + repr(tweet_s.sentiment) + Fore.RESET)
            else:
                print(Fore.RED + repr(tweet_s.sentiment) + Fore.RESET)
            print(str(self.total_sent))


        except Exception as e:
            print(str(e))
            pass
    def on_error(self, status):
        print('on_error: ' + str(status))

ts = TwitterSphere()
tstream = Stream(ts.auth, ts)
tstream.filter(track=['trump'], async=True)
