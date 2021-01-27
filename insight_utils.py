#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import SnowballStemmer
from langdetect import detect
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import string
import re
import pycountry
import nltk
import os
import numpy as np
import pandas as pd
"""
Created on Sun Jan 24 00:22:24 2021

@author: parashar
"""


# Import Libraries
from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import base64
from io import BytesIO

plt.style.use('ggplot')


table_name = "tweet_dump"
target = os.path.join('dbs', f'{table_name}.db')
loc_conn = f'sqlite:///{target}'
loc_engine = create_engine(loc_conn)


class tweet_meta:

    def percentage(self, part, whole):
        return 100 * float(part)/float(whole)

    def remove_rt(self, x):
        return re.sub(r'RT @\w+: ', " ", x)

    def rt(self, x):
        return re.sub(
            r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", x)

    def __init__(self, filter=True):
        self.df = pd.read_sql_table(table_name, con=loc_engine)
        self.df.drop_duplicates(inplace=True, subset=['txt'])
        if filter:
            self.df['txt'] = self.df['txt'].map(self.remove_rt).map(self.rt)
            self.df['txt'] = self.df['txt'].str.lower()
        tweets = self.df['txt'].to_list()
        #tweets = tweepy.Cursor(api.search, q=keyword).items(noOfTweet)
        self.positive = 0
        self.negative = 0
        self.neutral = 0
        self.polarity = 0
        self.tweet_list = []
        self.neutral_list = []
        self.negative_list = []
        self.positive_list = []

        for tweet in tweets:

            self.tweet_list.append(tweet)
            analysis = TextBlob(tweet)
            score = SentimentIntensityAnalyzer().polarity_scores(tweet)
            neg = score['neg']
            neu = score['neu']
            pos = score['pos']
            comp = score['compound']
            self.polarity += analysis.sentiment.polarity

            if neg > pos:
                self.negative_list.append(tweet)
                self.negative += 1
            elif pos > neg:
                self.positive_list.append(tweet)
                self.positive += 1
            elif pos == neg:
                self.neutral_list.append(tweet)
                self.neutral += 1

        self.noOfTweet = len(self.df)

        self.positive = self.percentage(self.positive, self.noOfTweet)
        self.negative = self.percentage(self.negative, self.noOfTweet)
        self.neutral = self.percentage(self.neutral, self.noOfTweet)
        self.polarity = self.percentage(self.polarity, self.noOfTweet)
        self.positive = format(self.positive, '.1f')
        self.negative = format(self.negative, '.1f')
        self.neutral = format(self.neutral, '.1f')

        # Number of Tweets (Total, Positive, Negative, Neutral)
        self.tweet_list = pd.DataFrame(self.tweet_list)
        self.neutral_list = pd.DataFrame(self.neutral_list)
        self.negative_list = pd.DataFrame(self.negative_list)
        self.positive_list = pd.DataFrame(self.positive_list)


def get_wordcloud_bs64():
    def create_wordcloud(text):
        _path = os.path.join('static', 'img', 'cloud.png')
        mask = np.array(Image.open(_path))
        stopwords = set(STOPWORDS)
        wc = WordCloud(background_color="white",
                       mask=mask,
                       max_words=3000,
                       stopwords=stopwords,
                       repeat=False)
        wc.generate(str(text))
        # wc.to_file("wc.png")
        # print("Word Cloud Saved Successfully")
        # path = "wc.png"
        # display(Image.open(path))
        return wc.to_image()

    x = tweet_meta()
    tw_list = pd.DataFrame(x.tweet_list)
    tw_list["text"] = tw_list[0]

    tw_list['text_len'] = tw_list['text'].astype(str).apply(len)
    tw_list['text_word_count'] = tw_list['text'].apply(
        lambda x: len(str(x).split()))

    # Removing Punctuation

    def remove_punct(text):
        text = "".join(
            [char for char in text if char not in string.punctuation])
        text = re.sub('[0-9]+', '', text)
        return text

    tw_list['punct'] = tw_list['text'].apply(lambda x: remove_punct(x))

    # Appliyng tokenization

    def tokenization(text):
        text = re.split(r'\W+', text)
        return text

    tw_list['tokenized'] = tw_list['punct'].apply(
        lambda x: tokenization(x.lower()))

    # Removing stopwords
    stopword = nltk.corpus.stopwords.words('english')

    def remove_stopwords(text):
        text = [word for word in text if word not in stopword]
        return text

    tw_list['nonstop'] = tw_list['tokenized'].apply(
        lambda x: remove_stopwords(x))

    # Appliyng Stemmer
    ps = nltk.PorterStemmer()

    def stemming(text):
        text = [ps.stem(word) for word in text]
        return text

    tw_list['stemmed'] = tw_list['nonstop'].apply(lambda x: stemming(x))

    # Cleaning Text

    def clean_text(text):
        # remove puntuation
        text_lc = "".join([word.lower()
                           for word in text if word not in string.punctuation])
        text_rc = re.sub('[0-9]+', '', text_lc)
        tokens = re.split(r'\W+', text_rc)    # tokenization
        # remove stopwords and stemming
        text = [ps.stem(word) for word in tokens if word not in stopword]
        return text

    # Appliyng Countvectorizer
    countVectorizer = CountVectorizer(analyzer=clean_text)
    countVectorizer.fit_transform(tw_list['text'])

    # Function to ngram
    def get_top_n_gram(corpus, ngram_range, n=None):
        vec = CountVectorizer(ngram_range=ngram_range,
                              stop_words='english').fit(corpus)
        bag_of_words = vec.transform(corpus)
        sum_words = bag_of_words.sum(axis=0)
        words_freq = [(word, sum_words[0, idx])
                      for word, idx in vec.vocabulary_.items()]
        words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
        return words_freq[:n]

    n2_bigrams = get_top_n_gram(tw_list['text'], (2, 2), 20)

    # n3_trigrams = get_top_n_gram(tw_list['text'], (3, 3), 20)
    # create_wordcloud(n3_trigrams)
    # return create_wordcloud(n2_bigrams)

    cloud = create_wordcloud(n2_bigrams)
    cloud_fig = BytesIO()
    cloud.save(cloud_fig, format='png')

    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(cloud_fig.getvalue()).decode('utf8')

    return pngImageB64String


def get_donut_bs64():

    x = tweet_meta()

    tw_list = pd.DataFrame(x.tweet_list)
    tw_list["text"] = tw_list[0]

    def remove_rt(x):
        return re.sub(r'RT @\w+: ', " ", x)

    def rt(x):
        return re.sub(
            r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", x)

    tw_list["text"] = tw_list.text.map(remove_rt).map(rt)
    tw_list["text"] = tw_list.text.str.lower()

    tw_list[['polarity', 'subjectivity']] = tw_list['text'].apply(
        lambda Text: pd.Series(TextBlob(Text).sentiment))
    for index, row in tw_list['text'].iteritems():
        score = SentimentIntensityAnalyzer().polarity_scores(row)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
        if neg > pos:
            tw_list.loc[index, 'sentiment'] = "negative"
        elif pos > neg:
            tw_list.loc[index, 'sentiment'] = "positive"
        else:
            tw_list.loc[index, 'sentiment'] = "neutral"
        tw_list.loc[index, 'neg'] = neg
        tw_list.loc[index, 'neu'] = neu
        tw_list.loc[index, 'pos'] = pos
        tw_list.loc[index, 'compound'] = comp

    tw_list.head(10)

    tw_list_negative = tw_list[tw_list["sentiment"] == "negative"]
    tw_list_positive = tw_list[tw_list["sentiment"] == "positive"]
    tw_list_neutral = tw_list[tw_list["sentiment"] == "neutral"]

    def count_values_in_column(data, feature):
        total = data.loc[:, feature].value_counts(dropna=False)
        percentage = round(data.loc[:, feature].value_counts(
            dropna=False, normalize=True)*100, 2)
        return pd.concat([total, percentage], axis=1, keys=['Total', 'Percentage'])

    count_values_in_column(tw_list, "sentiment")

    # create data for Pie Chart
    pc = count_values_in_column(tw_list, "sentiment")
    names = pc.index
    size = pc["Percentage"]

    # Create a circle for the center of the plot
    my_circle = plt.Circle((0, 0), 0.7, color='white')
    plt.pie(size, labels=names, colors=['green', 'blue', 'red'])
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    plt.tight_layout()
    donut_fig = BytesIO()
    plt.savefig(donut_fig, format='png')

    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(donut_fig.getvalue()).decode('utf8')

    return pngImageB64String


def get_pie_bs64():

    x = tweet_meta()

    keyword = 'Twitter'

    labels = ['Positive ['+str(x.positive)+'%]', 'Neutral [' +
              str(x.neutral)+'%]', 'Negative ['+str(x.negative)+'%]']
    sizes = [x.positive, x.neutral, x.negative]
    colors = ['yellowgreen', 'blue', 'red']
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(labels)
    plt.title("Sentiment Analysis Result for keyword=  "+keyword+"")
    plt.axis('equal')
    # plt.tight_layout()
    pi_fig = BytesIO()
    plt.savefig(pi_fig, format='png')

    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pi_fig.getvalue()).decode('utf8')

    return pngImageB64String


def get_donut_json():

    x = tweet_meta()

    _json = [
        {'name': 'positive', 'count': x.positive, 'percentage': x.positive},
        {'name': 'negative', 'count': x.negative, 'percentage': x.negative},
        {'name': 'neutral', 'count': x.neutral, 'percentage': x.neutral}
    ]
    return _json
