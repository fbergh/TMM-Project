# Data Retrieval

The data was retrieved with the [GetOldTweets-python repository](https://github.com/Jefferson-Henrique/GetOldTweets-python) due to the limitations that the Search Twitter API imposes on tweet retrieval. Namely, the Search API only allows retrieval of tweets up to a week old, while this research project requires tweets from 2014. The GetOldTweets-python repository was precisely written to overcome this issue and works very intuitively.

The data was simply retrieved by running

```bash
python Exporter.py --querysearch "#himtoo" --since 2010-01-01
```

in the command line (from the GetOldTweets-python repository) to obtain the *output_got_2018-09-22.csv* file and

```bash
python Exporter.py --querysearch "#himtoo" --since 2010-01-01 --until 2018-09-22
```

to obtain the *output_got_2014-01-01.csv* file. The retrieval was split into two phases because, for some reason, retrieval would halt after reaching 2018-09-22.

Note that the dataset retrieved by this repository might be incomplete, since this repository is not up-to-date (has not been updated in 2 years) and since I myself am not up-to-date on the internal workings of the repository. Furthermore, factors like tweet and account deletion play a role.
