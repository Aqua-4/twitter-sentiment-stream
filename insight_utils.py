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


def get_donut_bs64():
    def percentage(part, whole):
        return 100 * float(part)/float(whole)

    df = pd.read_sql_table(table_name, con=loc_engine)
    tweets = df['txt'].to_list()
    #tweets = tweepy.Cursor(api.search, q=keyword).items(noOfTweet)
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    tweet_list = []
    neutral_list = []
    negative_list = []
    positive_list = []

    for tweet in tweets:

        tweet_list.append(tweet)
        analysis = TextBlob(tweet)
        score = SentimentIntensityAnalyzer().polarity_scores(tweet)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
        polarity += analysis.sentiment.polarity

        if neg > pos:
            negative_list.append(tweet)
            negative += 1
        elif pos > neg:
            positive_list.append(tweet)
            positive += 1
        elif pos == neg:
            neutral_list.append(tweet)
            neutral += 1

    noOfTweet = len(df)

    positive = percentage(positive, noOfTweet)
    negative = percentage(negative, noOfTweet)
    neutral = percentage(neutral, noOfTweet)
    polarity = percentage(polarity, noOfTweet)
    positive = format(positive, '.1f')
    negative = format(negative, '.1f')
    neutral = format(neutral, '.1f')

    # Number of Tweets (Total, Positive, Negative, Neutral)
    tweet_list = pd.DataFrame(tweet_list)
    neutral_list = pd.DataFrame(neutral_list)
    negative_list = pd.DataFrame(negative_list)
    positive_list = pd.DataFrame(positive_list)
    print("total number: ", len(tweet_list))
    print("positive number: ", len(positive_list))
    print("negative number: ", len(negative_list))
    print("neutral number: ", len(neutral_list))

    keyword = 'Twitter'

    labels = ['Positive ['+str(positive)+'%]', 'Neutral [' +
              str(neutral)+'%]', 'Negative ['+str(negative)+'%]']
    sizes = [positive, neutral, negative]
    colors = ['yellowgreen', 'blue', 'red']
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(labels)
    plt.title("Sentiment Analysis Result for keyword=  "+keyword+"")
    plt.axis('equal')
    plt.tight_layout()
    figfile = BytesIO()
    plt.savefig(figfile, format='png')

    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(figfile.getvalue()).decode('utf8')

    return pngImageB64String
