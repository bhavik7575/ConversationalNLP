import pandas as pd # provide sql-like data manipulation tools. very handy.
from spacy.symbols import obj

pd.options.mode.chained_assignment = None
import numpy as np # high dimensional vector computing library.
from copy import deepcopy
from string import punctuation
from random import shuffle

import gensim
from gensim.models.word2vec import Word2Vec # the word2vec model gensim class
LabeledSentence = gensim.models.doc2vec.LabeledSentence # we'll talk about this down below

from keras.models import Sequential
from keras.layers import Dense, Activation
from nltk.corpus import stopwords
from tqdm import tqdm
tqdm.pandas(desc="progress-bar")

from nltk.tokenize import TweetTokenizer # a tweet tokenizer from nltk.

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

class TwitterSentimentAnalyzer(object):
    tokenizer = TweetTokenizer()
    x=1


    def __init__(self):
        print("TwitterSentimentAnalyzer Invoked")
        self.x=10
        self.tweet_w2v = Word2Vec.load("ConversationalService/Twitter_Sentiment_model_W2V")
        self.size=200
        self.model = Sequential()
        self.model.add(Dense(32, activation='relu', input_dim=200))
        self.model.add(Dense(2, activation='sigmoid'))
        self.model.compile(optimizer='rmsprop',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])
        #self.model.load_weights("ConversationalService/TwitterSentimentKerasModel.h5")
        self.model.load_weights("ConversationalService/TwitterSentimentKerasModelBinary.h5")
        self.modelWord2Vec=Word2Vec.load("ConversationalService/Twitter_Sentiment_model_W2V")
        #self.model=model
        return

    def getSentimentBinaryOutput(self,query):
        VectorToken = self.vectorize_query(query)
        #print(self.model.predict_proba(VectorToken))
        #sentiment=(self.model.predict_proba(VectorToken))
        SentimentArray=self.model.predict_proba(VectorToken)
        SentimentClass=np.argmax(SentimentArray)
        sentimentScore=np.max(SentimentArray)
        if SentimentClass :
            sentiment="Positive"
        else:
            sentiment="Negative"

        return sentiment,sentimentScore

    #
    # def getSentiment(self,query):
    #     VectorToken = self.vectorize_query(query)
    #     print(self.model.predict_proba(VectorToken))
    #     sentiment=(self.model.predict_proba(VectorToken))
    #
    #     if sentiment
    #     if SentimentClass :
    #         sentiment="Positive"
    #     else:
    #         sentiment="Negative"
    #
    #     return sentiment,sentimentScore

    def vectorize_query(self,utterence):
        vec = np.zeros(200).reshape((1, 200))
        words = self.Data_Cleaner(utterence)
        model =self.modelWord2Vec # Word2Vec.load("ConversationalService/Twitter_Sentiment_model_W2V")

        count = 0
        for word in words:
            try:
                vec += model.wv[word]
                count += 1
            except KeyError:
                continue
            if count != 0:
                vec /= count

        return vec

    def Data_Cleaner(self,sentence_text):
        lemmatize = True
        stem = False
        remove_stopwords = True

        stops = set(stopwords.words("english"))
        words = sentence_text.lower().split()
        # Optional stemmer
        if stem:
            stemmer = PorterStemmer()
            words = [stemmer.stem(w) for w in words]

        if lemmatize:
            lemmatizer = WordNetLemmatizer()
            words = [lemmatizer.lemmatize(w) for w in words]

        # Optionally remove stop words (false by default)
        if remove_stopwords:
            words = [w for w in words if not w in stops]

        return words

    def tokenize(tweet):
        try:
            tokenizer = TweetTokenizer()
            tweet = (tweet).lower()  # str(tweet.decode('utf-8').lower())
            tokens = tokenizer.tokenize(tweet)
            tokens = filter(lambda t: not t.startswith('@'), tokens)
            tokens = filter(lambda t: not t.startswith('#'), tokens)
            tokens = filter(lambda t: not t.startswith('http'), tokens)
            tokens = " ".join(tokens)
            token = tokens.split(" ")
            return token
        except:
            print("Exception occured")
        return 'NC'

class MyClass:
        Greeting = "Good Morning"
        def __init__(self, Name="there"):
            self.Greeting = Name + "!"
        def SayHello(self):
            print("Hello {0}".format(self.Greeting))