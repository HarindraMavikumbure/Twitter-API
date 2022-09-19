#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Harindra Sandun Mavikumbure and Scott Taylor
# Created Date: 9/15/2022
# ---------------------------------------------------------------------------
""" Uses the twitter API to extract tweets given a specific search query set in config.ini"""
# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
import tweepy as tw
import pandas as pd
import configparser


def save_tweets(search_query, api):
    """
    Searches twitter using its API and saves tweets in a list.

    Takes in API info and a search query, creates a cursor over tweets, iterates through its tweets, and stores them in
    a list.

    Parameters:
    search_query (string): a search query built from information in config.ini
    api(tweepy class): handles queries with twitter

    Returns:
    list: a list of tweets containing  user name, location, description, and verification status, date, text, hashtags,
    and source.

    """

    # create db cursor
    tweets = tw.Cursor(api.search,
                       q=search_query,
                       lang="en",
                       tweet_mode='extended').items(50)

    # store the API responses in a list
    tweets_copy = []
    for tweet in tweets:
        tweets_copy.append(tweet)

    print("Total Tweets fetched:", len(tweets_copy))
    return tweets_copy


def save_csv(tweet_list, csv_filename):
    """
    Saves a list of tweets as a CSV.

    Parameters:
    tweet_list(list): list of tweets containing user name, location, description, and verification status, date,
    text, hashtags, and source.

    Returns:
    csv: a csv of tweets containing the same information contained by the list

    """
    # initialize the dataframe
    tweets_df = pd.DataFrame()

    # populate the dataframe
    for tweet in tweet_list:
        hashtags = []
        try:
            for hashtag in tweet.entities["hashtags"]:
                hashtags.append(hashtag["text"])
            text = api.get_status(id=tweet.id, tweet_mode='extended').full_text
        except:
            pass
        tweets_dict = {'user_name': tweet.user.name,
                       'user_location': tweet.user.location,
                       'user_description': tweet.user.description,
                       'user_verified': tweet.user.verified,
                       'date': tweet.created_at,
                       'text': text,
                       'hashtags': [hashtags if hashtags else None],
                       'source': tweet.source,
                        'ID': tweet.id}
        tweets_df = pd.concat([tweets_df, pd.DataFrame(tweets_dict)], axis=0, ignore_index=True)
        tweets_df = tweets_df.reset_index(drop=True)

    # show the dataframe
    tweets_df.head()

    # save to csv
    tweets_df.to_csv(csv_filename + '.csv')


# config section, variables from config.ini
config = configparser.ConfigParser()
config.read('Twitter-API/config.ini')

# your Twitter API key and API secret
my_api_key = config["API"]['KEY']
my_api_secret = config["API"]['SECRET']

# get tweets by hashtags
# TODO build a search_query string builder for hashtags mentions, keywords
search_query = config["SEARCH"]['QUERY']
csv_filename = config["CSV"]["FILENAME"]

# authenticate
auth = tw.OAuthHandler(my_api_key, my_api_secret)
api = tw.API(auth, wait_on_rate_limit=True)


# run program. ideally with config the instructions can just be "run all cells"
if __name__ == "__main__":
    tweet_list = save_tweets(search_query, api)
    save_csv(tweet_list, csv_filename)
