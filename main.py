#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
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
import os


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


def save_csv(tweet_list, csv_directory, csv_filename):
    """
    Saves a list of tweets as a CSV.

    Parameters:
    tweet_list(list): list of tweets containing user name, location, description, and verification status, date,
    text, hashtags, and source.

    Returns:
    csv: a csv of tweets containing the same information contained by the list

    """
    print("Exporting to csv...")
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
        # add each tweet to a dataframe
        tweets_df = pd.concat([tweets_df, pd.DataFrame(tweets_dict)], axis=0, ignore_index=True)
        tweets_df = tweets_df.reset_index(drop=True)

    # show the dataframe
    tweets_df.head()

    # make user-specified directory
    if not os.path.exists(csv_directory):
        os.mkdir(csv_directory)

    # save to csv
    tweets_df.to_csv(csv_directory + '/' + csv_filename + '.csv')
    print("Exported")


# config section, variables from config.ini
config = configparser.ConfigParser()
config.read('Twitter-API/config.ini')

# your Twitter API key and API secret
my_api_key = config["API"]['KEY']
my_api_secret = config["API"]['SECRET']

# settings that decide whether to run search types
hash_search = config["SEARCH"]['HASH_SEARCH']
mention_search = config["SEARCH"]['MENTION_SEARCH']
key_search = config["SEARCH"]['KEY_SEARCH']

# Exclusions to add to string. defaults to empty string, always added to search string
exclude_rt = config["SEARCH"]['EXCLUDE_RT']
exclusions_string = ""
if exclude_rt == "1":
    exclusions_string = " -filter:retweets"

# directory name for CSV, will create a directory if a matching directory does not exist
csv_directory = config["CSV"]["DIRECTORY"]

# authenticate
auth = tw.OAuthHandler(my_api_key, my_api_secret)
api = tw.API(auth, wait_on_rate_limit=True)

if __name__ == "__main__":

    # create a list to hold lists, then create lists. Each list is composed of a CSV filename and a search string.
    all_queries = []
    if hash_search == "1":
        hash_list = ["tweets_by_hashtag"]
        hash_query = config["SEARCH"]['HASH_QUERY']
        hash_query += exclusions_string
        hash_list.append(hash_query)
        all_queries.append(hash_list)

    if mention_search == "1":
        mention_list = ["tweets_by_mention"]
        mention_query = config["SEARCH"]['MENTION_QUERY']
        mention_query += exclusions_string
        mention_list.append(mention_query)
        all_queries.append(mention_list)

    if key_search == "1":
        key_list = ["tweets_by_key"]
        key_query = config["SEARCH"]['KEY_QUERY']
        key_query += exclusions_string
        key_list.append(key_query)
        all_queries.append(key_list)

    # run api search and csv export methods for all queries
    for i in range(0, len(all_queries)):
        tweet_list = save_tweets(all_queries[i][1], api)
        save_csv(tweet_list, csv_directory, all_queries[i][0])
