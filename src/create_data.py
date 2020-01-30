# Import libraries
import pandas as pd
import os
from src.twitter_preprocessor import preprocess
import src.twitter_preprocessor as tpp

# See current working directory
print(os.getcwd())

# Initialise path to data
GOT_OUTPUT_PATH = "../private/"
DATA_PATH = "../data/"
delim = '|'

def load_all_tweets():
    tweets_0 = pd.read_csv(GOT_OUTPUT_PATH+"output_got_0.csv", sep=delim)
    tweets_1 = pd.read_csv(GOT_OUTPUT_PATH+"output_got_1.csv", sep=delim)
    tweets_2 = pd.read_csv(GOT_OUTPUT_PATH+"output_got_2.csv", sep=delim)
    tweets_3 = pd.read_csv(GOT_OUTPUT_PATH+"output_got_3.csv", sep=delim)
    # Append the two CSV files and drop "geo","mentions","hashtags", and all "Unnamed:x" columns
    # Then sort by (reformatted) date and reset index and save as new file
    tweets_all = tweets_0.append(tweets_1, ignore_index=True).append(tweets_2, ignore_index=True)\
                         .append(tweets_3, ignore_index=True)
    tweets_all = tweets_all.drop(["username","retweets","favorites","geo","mentions","id","permalink"], axis=1)
    # Remove hours and minutes and reformat date
    tweets_all["date"] = tweets_all["date"].apply(lambda s: s[:10])
    tweets_all.sort_values(by=["date"], inplace=True)
    tweets_all.reset_index(drop=True, inplace=True)
    return tweets_all

def preprocess_tweets(tweets):
    # Remove all retweets (tweets starting with RT)
    tweets = tweets[~tweets.text.str.contains("(\s)?rt\s", na=False, regex=True)]
    print("Pre-processing")
    tweets["processed_text"] = tweets["text"].apply(preprocess)
    print("Hashtags to lowercase")
    tweets["hashtags"] = tweets["hashtags"].astype(str).str.lower()
    # Drop empty tweets
    print("Drop empty tweets")
    tweets = tweets[tweets["processed_text"].astype(bool)]
    print("Drop duplicates")
    tweets = tweets.drop_duplicates(subset="processed_text")
    print("Produce clean text")
    # Clean text for word counts by removing punctuation and stopwords
    tweets["clean_text"] = tweets["processed_text"].apply(tpp.remove_punctuation).apply(tpp.remove_stopwords)
    return tweets

def main():
    tweets_all = load_all_tweets()
    tweets_all = preprocess_tweets(tweets_all)
    # Export the CSV file containing all pre-processed tweets
    tweets_all.to_csv(DATA_PATH+"tweets_all.csv", sep=delim)

    # Create CSV files for every time period I wish to research
    # 2015 and before
    tweets_period1 = tweets_all.loc[tweets_all['date'] < "2016"]
    tweets_period1.to_csv(DATA_PATH+"tweets_period1.csv", sep=delim)
    print(tweets_period1.head(), tweets_period1.shape)
    # 2016 - 14/10/17
    tweets_period2 = tweets_all.loc[(tweets_all['date'] < "2017-10-14")
                                        & (tweets_all['date'] > "2016")]
    tweets_period2.to_csv(DATA_PATH+"tweets_period2.csv", sep=delim)
    print(tweets_period2.head(), tweets_period2.shape)
    # 15/10/17 - 31/11/19
    tweets_period3 = tweets_all.loc[tweets_all['date'] > "2017-10-14"]
    tweets_period3.to_csv(DATA_PATH+"tweets_period3.csv", sep=delim)
    print(tweets_period3.head(), tweets_period3.shape)

if __name__ == '__main__':
    main()