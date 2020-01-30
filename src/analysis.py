from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import nltk
from nltk import tokenize as tkn
import src.twitter_preprocessor as tpp
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np

### CONSTANTS ###
DATA_PATH = "../data/"
IMG_PATH = "../img/"
sia = SentimentIntensityAnalyzer()
delim = '|'


### OPTIONS ###
pd.set_option('max_colwidth', 140)
pd.set_option('display.max_rows', 200)


### FUNCTIONS ###
def compute_sentiment(string):
    sentiment_value = sia.polarity_scores(string)["compound"]
    if sentiment_value >= 0.05:
        return 1
    if sentiment_value <= -0.05:
        return -1
    else:
        return 0

def plot_sentiment(axis, sentiment, is_show=False, is_save=True, filename="", title=""):
    axis.grid(zorder=0)
    axis.hist(sentiment, rwidth = 0.9, align = "left", bins = range(-1, 3), edgecolor = "black", zorder=3)
    axis.set_xticks(np.arange(-1, 2))
    axis.set_xticklabels(["Negative", "Neutral", "Positive"])
    axis.set_xlabel("Sentiment")
    axis.set_ylabel("Frequency")
    axis.set_title(title)
    # if is_save:
    #     plt.savefig(filename, bbox_inches="tight")
    # if is_show:
    #     plt.show()
    # plt.clf()

def compute_frequency_distribution(dataframe, target_col, top_k=20, is_bigram=False):
    freq_dist = nltk.FreqDist()
    if is_bigram:
        dataframe[target_col].apply(lambda target: freq_dist.update(nltk.bigrams(tkn.word_tokenize(target))))
    else:
        dataframe[target_col].apply(lambda target: freq_dist.update(nltk.tokenize.word_tokenize(target)))
    df_top_k = pd.DataFrame(freq_dist.most_common(top_k), columns = ['Targets', 'Frequency'])
    return df_top_k, freq_dist

def compute_hashtag_frequency_distribution(hashtags, top_k=20):
    # Compute hashtag frequency distribution
    hashtag_dist = nltk.FreqDist()
    hashtags.apply(lambda target: hashtag_dist.update(target.split(" ")))

    # Remove entries "#" and "#himtoo"
    hashtag_filter = ["#", "#himtoo"]
    filtered_hashtag_dist = dict((hashtag, freq) for hashtag, freq in hashtag_dist.items() if hashtag not in hashtag_filter)
    filtered_hashtag_dist = sorted(filtered_hashtag_dist.items(), key = lambda x: x[1], reverse = True)

    return pd.DataFrame(filtered_hashtag_dist[:top_k], columns = ['Targets', 'Frequency'])

def cooccuring_words(bigram_dist, target, threshold=50):
    return [bigram for bigram in list(bigram_dist.keys()) if target in bigram and bigram_dist[bigram] > threshold]

def plot_tweet_frequency(is_show=False, is_save=True):
    tweets_all = pd.read_csv(DATA_PATH+"tweets_all.csv", sep=delim)
    # Convert date column to datetime object and group frequency by year and month
    tweets_all["date"] = tweets_all["date"].astype("datetime64")
    stats_per_mon = tweets_all.groupby([tweets_all["date"].dt.year, tweets_all["date"].dt.month]).size()
    xlabels = stats_per_mon.index.to_flat_index().to_numpy()

    # Plot frequency with date labels every 4 months.
    ax = stats_per_mon.plot(kind="bar")
    ax.set_xticks(np.arange(len(stats_per_mon))[::4])
    ax.set_xticklabels(xlabels[::4], rotation=270)
    ax.set_xlabel("Dates (year, month)")
    ax.set_ylabel("Frequency")
    ax.set_title("The number of tweets per month containing #HimToo")
    if is_save:
        plt.savefig("../img/tweet_frequency.png", bbox_inches = "tight")
    if is_show:
        plt.show()
    plt.clf()

def compute_word_statistics(dataframe, top_k=20, is_cooccurrence=False):
    print(compute_hashtag_frequency_distribution(dataframe["hashtags"], top_k=top_k))

    # Compute and display uni- and bigram distributions
    unigrams_top_k, _ = compute_frequency_distribution(dataframe, "clean_text", top_k=top_k)
    bigrams_top_k, bigram_dist = compute_frequency_distribution(dataframe, "clean_text", is_bigram = True, top_k=top_k)
    print(unigrams_top_k)
    print(bigrams_top_k+"\n")

    if is_cooccurrence:
        # Specifically investigate specific words for co-occurence
        target_words = ["man", "men", "woman", "women", "story", "assault", "sex", "harassment", "movement", "abuse",
                        "victims", "rape", "climate", "son", "kavanaugh", "feminists"]
        for target in target_words:
            threshold = 50  # if target not in ["men","women"] else 75
            print("{:15} {}".format(target, cooccuring_words(bigram_dist, target, threshold)))

def main():
    tweets_p1 = pd.read_csv(DATA_PATH+"tweets_period1.csv", sep=delim)
    tweets_p2 = pd.read_csv(DATA_PATH+"tweets_period2.csv", sep=delim)
    tweets_p3 = pd.read_csv(DATA_PATH+"tweets_period3.csv", sep=delim)

    ### ALL PERIODS ###
    plot_tweet_frequency()

    # Compute sentiment
    tweets_p1["sentiment"] = tweets_p1["processed_text"].apply(compute_sentiment)
    tweets_p2["sentiment"] = tweets_p2["processed_text"].apply(compute_sentiment)
    tweets_p3["sentiment"] = tweets_p3["processed_text"].apply(compute_sentiment)

    # Plot and save sentiment distributions of every period
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows = 2, ncols = 2)
    plot_sentiment(ax1, tweets_p1["sentiment"], filename=IMG_PATH+"p1_sentiment.png",
                   title="Histogram of sentiment for tweets before 2016", is_show=True)
    plot_sentiment(ax2, tweets_p2["sentiment"], filename=IMG_PATH+"p2_sentiment.png",
                   title="Histogram of sentiment for tweets between 2016 and 14/10/2017")
    plot_sentiment(ax3, tweets_p3["sentiment"], filename=IMG_PATH+"p3_sentiment.png",
                   title="Histogram of sentiment for tweets after 14/10/2017")

    print("Tweets Period 1")
    compute_word_statistics(tweets_p1, top_k=10)
    print("\nTweets Period 2")
    compute_word_statistics(tweets_p2, top_k=10)
    print("\nTweets Period 3")
    compute_word_statistics(tweets_p3, is_cooccurrence = True)

    ### PERIOD 3 ###
    # Plot sentiment after removing meme
    tweets_p3 = tweets_p3[~tweets_p3["processed_text"].str.contains(r'be\smy\sson|#1|current\sclimate|son\sgraduate|go\ssolo|solo\sdate')]
    tweets_p3["sentiment"] = tweets_p3["processed_text"].apply(compute_sentiment)
    plot_sentiment(ax4, tweets_p3["sentiment"], filename = IMG_PATH + "p3_sentiment_wo_meme.png",
                   title = "Histogram of sentiment for tweets after 14/10/2017 without the meme")
    fig.set_size_inches(12, 8)
    plt.tight_layout()
    plt.savefig("../img/sentiments.png")

if __name__ == '__main__':
    main()