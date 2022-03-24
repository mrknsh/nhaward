import tweepy
import requests
import json

# Authenticate to Twitter
TWITTER_API_KEY = "Y5WIIKv6eF1MhHdXTjj5BgU74"
TWITTER_API_KEY_SECRET = "nm2kvMqOxhejlHXFCyfbinS5HP73rfAlAMxI3PBJae66eFsB1P"
TWITTER_ACCESS_TOKEN = "1365079173283393540-4QQiKp3jvwsAxy8njuynE2T0RI9K83"
TWITTER_ACCESS_TOKEN_SECRET = "VhZ20vV3DgE0uQcD9Hlet1z3NEfsCneT9WbcZ4Z8NWz3B"

class DOTweetStream(tweepy.Stream):

    def on_status(self, status):
        if status.text.lower().startswith("rt") == False and status.user.screen_name != "mediamadness22":
            link = "https://twitter.com/" + status.user.screen_name + "/status/" + str(status.id)
            # tweet each link
            headers = {'Content-type': 'application/json'}
            payload = {"text":str(link)}
            r = requests.post('https://hooks.slack.com/services/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', data=json.dumps(payload), headers=headers)
            print(r.text)



stream = DOTweetStream(
   TWITTER_API_KEY, TWITTER_API_KEY_SECRET,
   TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
)

stream.filter(track=["\"college media madness\"", "mediamadness", "collegemediamadness.com", "@mediamadness22"])


