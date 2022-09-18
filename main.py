# import tweepy
import tweepy as tw
import pandas as pd
import configparser


# TODO description
def save_tweets(search_query, api):
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


# TODO description
# TODO csv filename, path
def save_csv(tweet_list):
    # intialize the dataframe
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
                       'source': tweet.source}
        tweets_df = pd.concat([tweets_df, pd.DataFrame(tweets_dict)], axis=0, ignore_index=True)

        # TODO is this a nominal column? if so we should probably use tweet IDs instead, for peer review purposes
        tweets_df = tweets_df.reset_index(drop=True)

    # show the dataframe
    tweets_df.head()

    # save to csv
    tweets_df.to_csv('tweets_by_hashtags.csv')


# config section, variables from config.ini
config = configparser.ConfigParser()
config.read('Twitter-API/config.ini')
# your Twitter API key and API secret
my_api_key = config["API"]['KEY']
my_api_secret = config["API"]['SECRET']
search_query = config["SEARCH"]['QUERY']

# authenticate
auth = tw.OAuthHandler(my_api_key, my_api_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# TODO build a search_query string builder for hashtags mentions, keywords
# get tweets by hashtags

# section for running program. ideally with config the instructions can just be "run all cells"
tweet_list = save_tweets(search_query, api)
save_csv(tweet_list)

