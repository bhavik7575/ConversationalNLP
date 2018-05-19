import pandas as pd # provide sql-like data manipulation tools. very handy.
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

from tqdm import tqdm
tqdm.pandas(desc="progress-bar")

from nltk.tokenize import TweetTokenizer # a tweet tokenizer from nltk.
tokenizer = TweetTokenizer()

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
def ingest():
    print("Taking data")
    data = pd.read_csv('ConversationalService/Tweet_training.csv', names=["Sentiment","ItemID","Tsmtp","SentimentSource","sender","SentimentText"],encoding="ISO-8859-1")
    data.drop(['ItemID', 'SentimentSource'], axis=1, inplace=True)
    print("Data taken")
    data = data[data.Sentiment.isnull() == False]
    data['Sentiment'] = data['Sentiment'].map({4:1,0:0})
    data = data[data['SentimentText'].isnull() == False]
    data.reset_index(inplace=True)
    data.drop('Tsmtp', axis=1, inplace=True)
    data.drop('sender', axis=1, inplace=True)
    print('dataset loaded with shape', data.shape)
    return data

data = ingest()
data.head(5)

def tokenize(tweet):
    try:
        tweet = (tweet).lower()#str(tweet.decode('utf-8').lower())
        tokens = tokenizer.tokenize(tweet)
        tokens = filter(lambda t: not t.startswith('@'), tokens)
        tokens = filter(lambda t: not t.startswith('#'), tokens)
        tokens = filter(lambda t: not t.startswith('http'), tokens)
        tokens = " ".join(tokens)
        token=tokens.split(" ")
        return token
    except:
        print("Exception occured")
    return 'NC'

def postprocess(data, n=1000000):
    data = data.head(n)
    data['tokens'] = data['SentimentText'].progress_map(tokenize) ## progress_map is a variant of the map function plus a progress bar. Handy to monitor DataFrame creations.
    data = data[data.tokens != 'NC']
    data.reset_index(inplace=True)
    data.drop('index', inplace=True, axis=1)
    return data

data = postprocess(data)

x_train, x_test, y_train, y_test = train_test_split(np.array(data.head(data.__len__()).tokens),
np.array(data.head(data.__len__()).Sentiment), test_size=0.2)

def labelizeTweets(tweets, label_type):
    labelized = []
    for i,v in tqdm(enumerate(tweets)):
        label = '%s_%s'%(label_type,i)
        labelized.append(LabeledSentence(v, [label]))
    return labelized

x_train = labelizeTweets(x_train, 'TRAIN')
x_test = labelizeTweets(x_test, 'TEST')

#tweet_w2v = Word2Vec(size=200, min_count=10)
#tweet_w2v.build_vocab([x.words for x in tqdm(x_train)])

#tweet_w2v.train([x.words for x in tqdm(x_train)],total_examples=tweet_w2v.corpus_count,epochs=tweet_w2v.iter)
#tweet_w2v.save("Twitter_Sentiment_model")

tweet_w2v=Word2Vec.load("ConversationalService/Twitter_Sentiment_model_W2V")

print('building tf-idf matrix ...')
vectorizer = TfidfVectorizer(analyzer=lambda x: x, min_df=10)
matrix = vectorizer.fit_transform([x.words for x in x_train])
tfidf = dict(zip(vectorizer.get_feature_names(), vectorizer.idf_))
print('vocab size :', len(tfidf))

def buildWordVector(tokens, size):
    vec = np.zeros(size).reshape((1, size))
    count = 0.
    for word in tokens:
        try:
            vec += tweet_w2v[word].reshape((1, size)) * tfidf[word]
            count += 1.
        except KeyError: # handling the case where the token is not
        # in the corpus. useful for testing.
            continue

    if count != 0:
        vec /= count
    return vec

from sklearn.preprocessing import scale
n_dim=200
train_vecs_w2v = np.concatenate([buildWordVector(z, n_dim) for z in tqdm(map(lambda x: x.words, x_train))])
train_vecs_w2v = scale(train_vecs_w2v)

test_vecs_w2v = np.concatenate([buildWordVector(z, n_dim) for z in tqdm(map(lambda x: x.words, x_test))])
test_vecs_w2v = scale(test_vecs_w2v)

model = Sequential()
model.add(Dense(32, activation='relu', input_dim=200))
model.add(Dense (1, activation='sigmoid'))
model.compile(optimizer='rmsprop',
loss='binary_crossentropy',
metrics=['accuracy'])

model.fit(train_vecs_w2v, y_train, epochs=9, batch_size=32, verbose=2)

score = model.evaluate(test_vecs_w2v, y_test, batch_size=128, verbose=2)
print(score[1])
