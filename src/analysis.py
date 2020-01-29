from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import nltk
from nltk import tokenize as tkn
import src.twitter_preprocessor as tpp
import matplotlib.pyplot as plt
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

def plot_sentiment(sentiment, is_show=False, is_save=True, filename="", title=""):
    plt.grid(zorder=0)
    plt.hist(sentiment, rwidth = 0.9, align = "left", bins = range(-1, 3), edgecolor = "black", zorder=3)
    plt.xticks(np.arange(-1, 2), ["Negative", "Neutral", "Positive"])
    plt.xlabel("Sentiment")
    plt.ylabel("Frequency")
    plt.title(title)
    if is_save:
        plt.savefig(filename, bbox_inches="tight")
    if is_show:
        plt.show()

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

    return pd.DataFrame(filtered_hashtag_dist[:20], columns = ['Targets', 'Frequency'])

def cooccuring_words(bigram_dist, target, threshold=50):
    return [bigram for bigram in list(bigram_dist.keys()) if target in bigram and bigram_dist[bigram] > threshold]

def main():
    tweets_p1 = pd.read_csv(DATA_PATH+"tweets_period1.csv", sep=delim)
    tweets_p2 = pd.read_csv(DATA_PATH+"tweets_period2.csv", sep=delim)
    tweets_p3 = pd.read_csv(DATA_PATH+"tweets_period3.csv", sep=delim)

    ### ALL PERIODS ###
    # Compute sentiment
    tweets_p1["sentiment"] = tweets_p1["processed_text"].apply(compute_sentiment)
    tweets_p2["sentiment"] = tweets_p2["processed_text"].apply(compute_sentiment)
    tweets_p3["sentiment"] = tweets_p3["processed_text"].apply(compute_sentiment)

    # Plot and save sentiment distributions of every period
    plot_sentiment(tweets_p1["sentiment"], filename=IMG_PATH+"p1_sentiment.png",
                   title="Histogram of sentiment for tweets before 2016")
    plot_sentiment(tweets_p2["sentiment"], filename=IMG_PATH+"p2_sentiment.png",
                   title="Histogram of sentiment for tweets between 2016 and 14/10/2017")
    plot_sentiment(tweets_p3["sentiment"], filename=IMG_PATH+"p3_sentiment.png",
                   title="Histogram of sentiment for tweets after 14/10/2017")

    ### PERIOD 3 ###
    # Clean text for word counts by removing "my son"-meme, punctuation, and stopwords
    tweets_p3 = tweets_p3[~tweets_p3["processed_text"].str.contains(r'be\smy\sson')]
    tweets_p3["clean_text"] = tweets_p3["processed_text"].apply(tpp.remove_punctuation).apply(tpp.remove_stopwords)

    # Plot sentiment after removing meme
    tweets_p3["sentiment"] = tweets_p3["processed_text"].apply(compute_sentiment)
    plot_sentiment(tweets_p3["sentiment"], filename=IMG_PATH+"p3_sentiment_wo_meme.png",
                   title="Histogram of sentiment for tweets after 14/10/2017 without the my son meme")

    # Compute and display uni- and bigram distributions
    unigrams_top_k, _ = compute_frequency_distribution(tweets_p3, "clean_text")
    bigrams_top_k, bigram_dist = compute_frequency_distribution(tweets_p3, "clean_text", is_bigram = True)
    print(unigrams_top_k)
    print(bigrams_top_k)

    # Specifically investigate specific words for co-occurence
    target_words = ["man", "men", "woman", "women", "feminists", "story", "assault", "sex", "harassment", "movement",
                    "abuse", "victims", "rape", "climate", "solo", "son", "kavanaugh"]
    for target in target_words:
        threshold = 50  # if target not in ["men","women"] else 75
        print("{:15} {}".format(target, cooccuring_words(bigram_dist, target, threshold)))

if __name__ == '__main__':
    main()