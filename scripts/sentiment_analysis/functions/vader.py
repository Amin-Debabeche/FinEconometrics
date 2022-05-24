import os
import re
import pandas as pd
from time import time
import datetime
import numpy as np
import spacy
import nltk
import wrds
import spacy
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf
from tqdm import tqdm
import textblob

## Sentiment Analyser

from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
from flair.models import TextClassifier
from flair.data import Sentence
classifier = TextClassifier.load('en-sentiment')

def sentiment_analyser(df, v=True, f=False, b=False, r_vader=0.8, r_fler=0.1, r_blob=0.1):
    
    df_fler, df_vader, df_blob = [], [], []
    for sentence in tqdm(df['body'], position=0):
        if v:
            df_vader.append(vader(sentence))
        if f:
            df_fler.append(fler(sentence))
        if b:
            df_blob.append(blob(sentence))
    if v: 
        df['VADER'] = df_vader
    if f: 
        df['FLAIR'] = df_fler
    if b:
        df['BLOB'] = df_blob

    if v and f and b:
        df['compound'] = df['VADER']*r_vader + \
            df['FLAIR']*r_fler + df['BLOB']*r_blob
    elif v and f and not b:
        df['compound'] = df['VADER']*(r_vader+r_blob) + df['FLAIR']*r_fler
    elif v and b and not f:
        df['compound'] = df['VADER']*(r_vader+r_fler) + df['BLOB']*r_blob
    else:
        df['compound'] = df['VADER']

    return df


def vader(sentence):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(sentence)['compound']
    return float(sentiment)


def fler(sentence):
    s = Sentence(sentence)
    classifier.predict(s)
    sentiment = str(s.labels[0])
    num = float(re.findall(r'\d+\.\d+', sentiment)[0])
    if sentiment.find('POSITIVE') == -1:
        num = num * -1
    return num


def blob(sentence):
    sentiment = TextBlob(sentence).sentiment.polarity
    return sentiment


Twitter_preprocessed_data = sentiment_analyser(Twitter_preprocessed_data)

import multiprocessing

n_splits = 8
n_rows = len(Twitter_preprocessed_data)
chunks = [[int(i * n_rows/n_splits), int((i+1) * n_rows/n_splits)]  for i in range(n_splits)]

# function to perform vader analysis on portion of the table
def vader_worker(row_range):
    return sentiment_analyser(Twitter_preprocessed_data.iloc[row_range[0]:row_range[1]])

p = multiprocessing.Pool(processes=n_splits) 
Twitter_preprocessed_data = p.map(vader_worker, chunks)
p.close() 
del p