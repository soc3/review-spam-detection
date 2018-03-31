import pandas as pd
import string
from nltk.corpus import stopwords
import json
import features
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

def preprocess(mess):
    nopunc = [c for c in mess if c not in string.punctuation]
    nopunc = ''.join(nopunc)
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

#Saving data into a dataframe from the text file
with open("Data/TrainingSet") as fh:
    data = json.load(fh)
df = pd.DataFrame(data)
df.columns = ["review_id", "hotel_name", "review", "polarity", "spam"]

a = []
b = []
c = []
d = []
e = []
f2 = []
g = []
h = []
i = []
j = []
k = []
l = []
for f in df["review"].head(1000):
    a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12 = features.majorfunc(f)
    a.append(a1)
    b.append(a2)
    c.append(a3)
    d.append(a4)
    e.append(a5)
    f2.append(a6)
    g.append(a7)
    h.append(a8)
    i.append(a9)
    j.append(a10)
    k.append(a11)
    l.append(a12)
dfd = df.head(1000)
dfd["num_of_words"] =a
dfd["avg_words_per_sent"]=b
dfd["unique_words"]=c
dfd["self_words"]=d
dfd["brand"]=e
dfd["avg_word_length"]=f2
dfd["connectors"]=g
dfd["digits"]=h
dfd["verbs_per_noun"]=i
dfd["adj"]=j
dfd["prep"]=k
dfd["adverb"]=l

df["hotel_name"] = le.fit_transform(df["hotel_name"])
#Ratios define the spam content in the review
dfd.remove("review")

print(dfd.head(5))
