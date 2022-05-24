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
import preprocessing
import text_cleaning

RANDOM_SEED = 7
DATA_DIR = "../data"
INTERM_DIR = '../compiled data'

# note: wsb=wallstreetbets
twitter_data_path = os.path.join(DATA_DIR, 'XXX_raw.csv')
bitcoin_data_path = os.path.join(DATA_DIR, 'XXX')

# efficiency and accuracy --> "en_core_web_trf"
nlp = spacy.load("en_core_web_sm")

# Define functions to load our data

def load_twitter_data(data_path, nrows=None, cols=['id', 'text','created_utc', 'likes', 'link_id', 'is_submitter']):
    "Load twitter data, nrows None indicates all rows, otherwise specified integer of rows"
    data = pd.read_csv(twitter_data_path, nrows = nrows, delimiter=',', usecols=cols)
    
    data = data[data['author'] != '']
    data = data[data['body'] != '']
    
    data['created_utc'] = pd.to_numeric(data['created_utc'], errors='coerce')
    data = data.dropna(subset=['created_utc'])
    data['created_utc'] = data['created_utc'].astype(int)

    data['created_utc'] = data['created_utc'].apply(lambda x: datetime.datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
    data = data.loc[data['created_utc'] > '2000']
    return data

def load_stock_bitcoin(ticker):
    permco = permcos[permcos.ticker == ticker].permco.values[0]
    # to 2021-03-25 ??
    asset = pd.read_csv(bitcoin_data_path)   
    asset = asset.dropna()
    asset["log_ret"] = np.log(asset.prc).diff(1)

    return asset["log_ret"]

# Plot of data points per day
twitter_df = load_twitter_data(twitter_data_path, nrows=None)
twitter_df.groupby(twitter_df["created_utc"].apply(lambda x: datetime.datetime.fromisoformat(x)).dt.day).count().plot(kind="bar")

Twitterpreprocessing = preprocessing(
    twitter_df, lemmatize=None, lower_case=True, rem_stopwords=True, rem_punctuation=True)
Twitterpreprocessing.clean_textual_data('body')
useful_columns = ['author', 'body', 'created_utc',
                  'score', 'link_id', 'is_submitter']
Twitter_preprocessed_data = Twitterpreprocessing.data[useful_columns]

Twitter_preprocessed_data = text_cleaning.rem_url_at(Twitter_preprocessed_data)
Twitter_preprocessed_data = text_cleaning.tagging(Twitter_preprocessed_data)

Twitter_preprocessed_data.replace('', np.nan, inplace=True)
Twitter_preprocessed_data = Twitter_preprocessed_data.dropna(how='any', axis=0)
Twitter_preprocessed_data = Twitter_preprocessed_data[Twitter_preprocessed_data['body'].map(
    lambda d: len(d)) > 0]
