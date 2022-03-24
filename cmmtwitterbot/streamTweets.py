import tweepy
import requests
import json

# Authenticate to Twitter
TWITTER_API_KEY = "xxx"
TWITTER_API_KEY_SECRET = "xxx"
TWITTER_ACCESS_TOKEN = "xxx"
TWITTER_ACCESS_TOKEN_SECRET = "xxx"

class DOTweetStream(tweepy.Stream):

    def on_status(self, status):
        if status.text.lower().startswith("rt") == False and status.user.screen_name != "mediamadness22":
            link = "https://twitter.com/" + status.user.screen_name + "/status/" + str(status.id)
            # tweet each link
            headers = {'Content-type': 'application/json'}
            payload = {"text":str(link)}
            r = requests.post('xxx', data=json.dumps(payload), headers=headers)
            print(r.text)



stream = DOTweetStream(
   TWITTER_API_KEY, TWITTER_API_KEY_SECRET,
   TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
)

stream.filter(track=["\"college media madness\"", "mediamadness", "collegemediamadness.com", "@mediamadness22"])


