'''
Retrieved and adapted from: https://github.com/vasisouv/tweets-preprocessor
'''

import string

import nltk
from nltk.corpus import stopwords
from nltk import re
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

wnl = WordNetLemmatizer()

def get_hashtags_pattern():
    return re.compile(r'#\w*')

def get_single_letter_words_pattern():
    return re.compile(r'(?<![\w\-])\w(?![\w\-])|[…’‘]')

def get_mentions_pattern():
    return re.compile(r'@\w*')

def get_twitter_reserved_words_pattern():
    return re.compile(r'\brt\b|\bfav\b|\bvia\b|\btatus\b|\batus\b|\btus\b|\bus\b')

def preprocess(text):
    text = text.lower()
    text = remove_urls(text)
    text = remove_twitter_reserved_words(text)
    text = remove_mentions(text)
    text = remove_hashtags(text)
    # text = remove_punctuation(text))
    text = remove_alphanumeric_strings(text)
    text = remove_single_letter_words(text)
    # text = remove_stopwords(text)
    return lemmatise(text)

def remove_urls(text):
    text = re.sub(r"pic.twitter.com\/[a-zA-Z0-9]*", '', text)
    text = re.sub(r"https?\s?:\/\/\s?([a-zA-Z]+\.)?\s?[a-zA-Z]+\.\s?[a-zA-Z]+\/?", '', text)
    text = re.sub(r"\/+[A-Za-z0-9\-_]+", '', text)
    return text

def remove_twitter_reserved_words(text):
    return re.sub(pattern=get_twitter_reserved_words_pattern(), repl='', string=text)

def remove_mentions(text):
    return re.sub(pattern=get_mentions_pattern(), repl='', string=text)

def remove_hashtags(text):
    return re.sub(pattern=get_hashtags_pattern(), repl='', string=text)

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def remove_single_letter_words(text):
    return re.sub(pattern=get_single_letter_words_pattern(), repl='', string=text)

def remove_alphanumeric_strings(text):
    return re.sub(r'(\w+\d+|\d+\w+)+|\d{10,}|[a-zA-Z0-9]{20,}|(\d*[a-zA-Z\-_]+\d+[a-zA-Z\-_]*)+|([a-zA-Z0-9]+-)+[a-zA-Z0-9]*', '', text)


def remove_stopwords(text, extra_stopwords=[]):
    text = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))

    new_sentence = []
    for w in text:
        if w not in stop_words and w not in extra_stopwords:
            new_sentence.append(w)
    return ' '.join(new_sentence)

def lemmatise(text):
    words = word_tokenize(text)
    lemmatised_words = [wnl.lemmatize(word, pos="v") for word in words]
    return " ".join(lemmatised_words)
