#%%
# Import libraries
import pandas as pd
import os
# See current working directory
print(os.getcwd())

# Initialise path to data
DATA_PATH = "TMM_project/data/"

#%%
tweets_to2018 = pd.read_csv(DATA_PATH+"output_got_2014-01-01.csv", sep=';')
tweets_to2018.head()

#%%
tweets_from2018 = pd.read_csv(DATA_PATH+"output_got_2018-09-22.csv", sep=';')
tweets_from2018.head()

#%%
# Append the two CSV files and drop "geo","mentions","hashtags", and all "Unnamed:x" columns
# Then sort by date and reset index and save as new file
# TODO: reformat date such that sorting is chronological
tweets_all = tweets_from2018.append(tweets_to2018, ignore_index=True)
tweets_all = tweets_all.drop(tweets_all.columns[[0,1,2,3,4,7]], axis=1)
tweets_all.sort_values(by=["date"], inplace=True)
tweets_all.reset_index(drop=True, inplace=True)
# tweets_all.to_csv(DATA_PATH+"tweets_all.csv")

# %%
