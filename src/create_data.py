#%%
# Import libraries
import pandas as pd
import os
import sys
from src.twitter_preprocessor import custom_preprocess
# See current working directory
print(os.getcwd())

# Initialise path to data
DATA_PATH = "../data/"

#%%
tweets_to2018 = pd.read_csv(DATA_PATH+"output_got_2014-01-01.csv", sep=';')
print(tweets_to2018.head())

#%%
tweets_from2018 = pd.read_csv(DATA_PATH+"output_got_2018-09-22.csv", sep=';')
print(tweets_from2018.head())

#%%
def dateToISO8601(date):
    '''Converts date from "day/month/year"-format to "year/month/day"-format (ISO8601)'''
    day, month, year = date.split("/")
    return year+"/"+month+"/"+day

#%%
# Append the two CSV files and drop "geo","mentions","hashtags", and all "Unnamed:x" columns
# Then sort by (reformatted) date and reset index and save as new file
tweets_all = tweets_from2018.append(tweets_to2018, ignore_index=True)
tweets_all = tweets_all.drop(tweets_all.columns[[0,1,2,3,4,7]], axis=1)
# Remove hours and minutes and reformat date
tweets_all["date"] = tweets_all["date"].apply(lambda s: s[:10]).apply(dateToISO8601)
tweets_all.sort_values(by=["date"], inplace=True)
tweets_all.reset_index(drop=True, inplace=True)

#%%
# Pre-process tweets
tweets_all["text"] = tweets_all["text"].apply(custom_preprocess)
tweets_all = tweets_all[tweets_all["text"].astype(bool)]
print(tweets_all.head(10))

#%%
# Finally export the CSV file containing all pre-processed tweets
tweets_all.to_csv(DATA_PATH+"tweets_all.csv")

#%%
# Create CSV files for every time period I wish to research
# 2015 and before
tweets_2015bf = tweets_all.loc[tweets_all['date'] < "2016"]
tweets_2015bf.to_csv(DATA_PATH+"tweets_2015-and-before.csv")
print(tweets_2015bf.head())
#%%
# 2016 - 14/10/17
tweets_2016to20171014 = tweets_all.loc[(tweets_all['date'] < "2017/10/14") 
                                     & (tweets_all['date'] > "2016")]
tweets_2016to20171014.to_csv(DATA_PATH+"tweets_2016-to-20171014.csv")
print(tweets_2016to20171014.head())
#%%
# 15/10/17 - 31/11/19
tweets_20171015to20191131 = tweets_all.loc[tweets_all['date'] > "2017/10/14"]
tweets_20171015to20191131.to_csv(DATA_PATH+"tweets_20171015-to-20191131.csv")
print(tweets_20171015to20191131.head())
