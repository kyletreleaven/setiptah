# https://developers.google.com/api-client-library/python/guide/aaa_oauth

#import json
import yaml
import tweepy


def show_public(api):
	public_tweets = api.home_timeline()
	for tweet in public_tweets:
	    print tweet.text


if __name__ == '__main__':

	with open('client.yaml','r') as f:
		client_data = yaml.load(f)

	consumer_key = client_data['consumer_key']
	consumer_secret = client_data['consumer_secret']

	access_token = client_data['access_token']
	access_token_secret = client_data['access_token_secret']

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)
