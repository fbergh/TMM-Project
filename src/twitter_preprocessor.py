'''
Retrieved and adapted from: https://github.com/vasisouv/tweets-preprocessor
'''

import string

import nltk
from nltk.corpus import stopwords
from nltk import re

MIN_YEAR = 1900
MAX_YEAR = 2100


def get_url_patern():
    return re.compile(
        r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))'
        r'[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})')


def get_emojis_pattern():
    try:
        # UCS-4
        emojis_pattern = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    except re.error:
        # UCS-2
        emojis_pattern = re.compile(
            u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
    return emojis_pattern


def get_hashtags_pattern():
    return re.compile(r'#\w*')


def get_single_letter_words_pattern():
    return re.compile(r'(?<![\w\-])\w(?![\w\-])')


def get_blank_spaces_pattern():
    return re.compile(r'\s{2,}|\t')


def get_twitter_reserved_words_pattern():
    return re.compile(r'(RT|rt|FAV|fav|VIA|via)')


def get_mentions_pattern():
    return re.compile(r'@\w*')


def is_year(text):
    if (len(text) == 3 or len(text) == 4) and (MIN_YEAR < len(text) < MAX_YEAR):
        return True
    else:
        return False

def custom_preprocess(text):
    return remove_stopwords(remove_blank_spaces(remove_single_letter_words(remove_punctuation(
                            remove_twitter_reserved_words(remove_hashtags(remove_mentions(remove_urls(text))))))))

def fully_preprocess(text):
        return remove_urls(text) \
            .remove_mentions(text) \
            .remove_hashtags(text) \
            .remove_twitter_reserved_words(text) \
            .remove_punctuation(text) \
            .remove_single_letter_words(text) \
            .remove_blank_spaces(text) \
            .remove_stopwords(text) \
            .remove_numbers(text)

def remove_urls(text):
    return re.sub(pattern=get_url_patern(), repl='', string=text)


def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))


def remove_mentions(text):
    return re.sub(pattern=get_mentions_pattern(), repl='', string=text)


def remove_hashtags(text):
    return re.sub(pattern=get_hashtags_pattern(), repl='', string=text)


def remove_twitter_reserved_words(text):
    return re.sub(pattern=get_twitter_reserved_words_pattern(), repl='', string=text)


def remove_single_letter_words(text):
    return re.sub(pattern=get_single_letter_words_pattern(), repl='', string=text)


def remove_blank_spaces(text):
    return re.sub(pattern=get_blank_spaces_pattern(), repl=' ', string=text)


def remove_stopwords(text, extra_stopwords=None):
    if extra_stopwords is None:
        extra_stopwords = []
    text = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))

    new_sentence = []
    for w in text:
        if w not in stop_words and w not in extra_stopwords:
            new_sentence.append(w)
    return ' '.join(new_sentence)


def remove_numbers(text, preserve_years=False):
    text_list = text.split(' ')
    for text in text_list:
        if text.isnumeric():
            if preserve_years:
                if not is_year(text):
                    text_list.remove(text)
            else:
                text_list.remove(text)

    return ' '.join(text_list) 


def lowercase(text):
    return text.lower()
