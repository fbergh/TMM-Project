# Data Retrieval

[GetOldTweets-python repository](https://github.com/Jefferson-Henrique/GetOldTweets-python) was used to retrieve the tweet data due to the limitations that the Search Twitter API imposes on tweet retrieval. Twitter's Search API only allows retrieval of tweets up to a week old, while this research project requires tweets from 2014. The GetOldTweets-python repository was written to overcome this issue.

The data was retrieved by running

```bash
python Exporter.py --querysearch "#himtoo" --since 2010-01-01
```

in the command line (from the GetOldTweets-python repository) to obtain tweets from 2018-09-22. To retrieve the tweets before this date, the following command was executed:

```bash
python Exporter.py --querysearch "#himtoo" --since 2010-01-01 --until 2018-09-22
```

The retrieval was split into two phases because, for some reason, retrieval would halt after reaching 2018-09-22.

Note that the dataset retrieved by this repository might be incomplete, since this repository is not up-to-date (has not been updated in 2 years) and since I am not up-to-date on the internal workings of the repository. Furthermore, factors like tweet and account deletion over time might have reduced the number of tweets.
