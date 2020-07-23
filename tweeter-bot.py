from tweepy import API, OAuthHandler, TweepError, Stream, StreamListener
from secrets import *
import random
import os
import re


auth = OAuthHandler(
    consumer_key=consumer_key, consumer_secret=consumer_secret)
auth.set_access_token(key=access_token_key, secret=access_token_secret)

api = API(auth, wait_on_rate_limit=True)

watch_list = ['#100DaysOfCode', '#codeNewbie',
              '#WomenWhoCode', '#javascript']
reply_list = ['#100DaysOfCode', '#codeNewbie']
me = api.me().screen_name

with open(os.path.dirname(__file__)+'/replies.txt', 'r') as f:
    replies = f.readlines()


class Listener(StreamListener):

    def on_error(self, status_code):
        print('error', status_code)

    def on_status(self, status):
        data = status._json
        random.shuffle(replies)
        index = random.randint(0, len(replies)-1)
        reply = replies[index].replace('###', data['user']['screen_name'])
        if me == data['user']['screen_name']:
            print("Won't retweet own tweet")
        else:
            if data['in_reply_to_status_id'] == None:
                if 'retweeted_status' not in data.keys():

                    try:
                        # Only reply if any of the hashtags in @reply_list is present
                        if 1 in [1 if i in data['text'] else 0 for i in reply_list]:
                            # Reply if the tweet contain Day [digit]
                            if re.search("Day\s*\d+"):
                                api.update_status(reply, data['id'])
                            else:
                                print('Not a relevant Update')
                        # Like the tweet
                        api.create_favorite(data['id'])
                        # Follow the Poster
                        api.create_friendship(data['user']['screen_name'])
                        # Finally retweet
                        api.retweet(data['id'])
                    except TweepError:
                        print('Tweet already retweeted')
                else:
                    print("Not allowed to retweet a retweet")
            else:
                print('Just a Commnent')


mylistner = Listener()
stream = Stream(auth=api.auth, listener=mylistner)
stream.filter(track=watch_list)
