import pandas as pd
import string
from nltk.corpus import stopwords

def preprocess(mess):
    nopunc = [c for c in mess if c not in string.punctuation]
    nopunc = ''.join(nopunc)
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

#Saving data into a dataframe from the text file
data = pd.read_csv('reviewContent', sep="\t", header=None)
data.columns = ["user_id", "prod_id", "date", "review"]

#Removing unwanted characters from date
data['date'] = data['date'].replace(['-'], [''], regex=True)

#PROCESSING THE REVIEWS
data['review'] = data['review'].head(5).apply(preprocess)

print(data.head())
