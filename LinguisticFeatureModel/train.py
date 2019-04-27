import pandas as pd
import numpy as np
import string
from nltk.corpus import stopwords
import json
import features
import nltk

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

with open("./Data/TrainingSet") as fh:
    data = json.load(fh)
df = pd.DataFrame(data)
df.columns = ["review_id", "hotel_name", "review", "polarity", "spam"]

iterator = 0
df["num_of_words"] = np.nan
df["avg_words_per_sent"]=np.nan
df["unique_words"]=np.nan
df["self_words"]=np.nan
df["brand"]=np.nan
df["avg_word_length"]=np.nan
df["connectors"]=np.nan
df["digits"]=np.nan
df["verbs_per_noun"]=np.nan
df["adj"]=np.nan
df["prep"]=np.nan
df["adverb"]=np.nan
#Iterating through whole data-set to add linguistic features
for review in df["review"]:
    a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12 = features.majorfunc(review)
    df.iloc[iterator, df.columns.get_loc('num_of_words')] = a1
    df.iloc[iterator, df.columns.get_loc('avg_words_per_sent')] = a2
    df.iloc[iterator, df.columns.get_loc('unique_words')] = a3
    df.iloc[iterator, df.columns.get_loc('self_words')] = a4
    df.iloc[iterator, df.columns.get_loc('brand')] = a5
    df.iloc[iterator, df.columns.get_loc('avg_word_length')] = a6
    df.iloc[iterator, df.columns.get_loc('connectors')] = a7
    df.iloc[iterator, df.columns.get_loc('digits')] = a8
    df.iloc[iterator, df.columns.get_loc('verbs_per_noun')] = a9
    df.iloc[iterator, df.columns.get_loc('adj')] = a10
    df.iloc[iterator, df.columns.get_loc('prep')] = a11
    df.iloc[iterator, df.columns.get_loc('adverb')] = a12
    iterator += 1
#Label Encoding
df["hotel_name"] = le.fit_transform(df["hotel_name"].astype('str'))
#One-hot encoding
just_dummies = pd.get_dummies(df['hotel_name'])
#Adding the encoded feature vectors and removing the categorical feature column
df = pd.concat([df, just_dummies], axis=1)      
df.drop(['hotel_name'], inplace=True, axis=1)

df.drop(['review_id'],axis=1,inplace=True)
df.drop(['review'],axis=1,inplace=True)

X_train, X_test, y_train, y_test = train_test_split(df.loc[:, df.columns != 'spam'], 
                                                    df['spam'], test_size=0.2,random_state=1)
print(X_train.shape, X_test.shape,y_train.shape)
y_train = y_train.to_frame()
y_test = y_test.to_frame()
print(type(y_test))

from sklearn.model_selection import GridSearchCV
from sklearn import svm
svc = svm.SVC()
parameters = {'kernel':('linear','rbf'), 'C':[1,10]}
clf=GridSearchCV(svc,parameters,cv=10)
model = clf.fit(X_train,y_train.values.ravel())
print ("Score:", model.score(X_test, y_test.values.ravel()))   
