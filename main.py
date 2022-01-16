import os
import tweepy
from twitchAPI.twitch import Twitch

def tweet(update):
  t = tweepy.Client(
    access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
    access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'),
    consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
    consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET')
  )
  t.create_tweet(text=update)

twitch = Twitch(os.environ.get('TWITCH_CLIENT_ID'), os.environ.get('TWITCH_CLIENT_SECRET'))

# get ID of user
user_info = twitch.get_users(logins=[os.environ.get('TWITCH_USERNAME')])['data']
if len(user_info)== 0:
    print("ERROR: user not found")
    exit(0)
user_id = user_info[0]['id']

# get stream is live
stream_infos = twitch.get_streams(user_id=[user_id])['data']
if len(stream_infos) == 0:
    print("ERROR: user is not streaming")
    exit(0)
stream_info = stream_infos[0]

# tweet
title = stream_info['title']
url = "https://www.twitch.tv/" + stream_info['user_login']
hash_tag = "#" + stream_info['game_name'].replace(" ", "")

print("title: %s\ntag: %s\nurl: %s" % (title, hash_tag, url))
tweet("🔴LIVE: %s\n%s\n%s" % (title, hash_tag, url))
