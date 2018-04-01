from __future__ import division

print('-'*50)

#Importing Dependecies---------------------------------------------------
import collections
import nltk
from collections import Counter
from nltk.corpus import brown
from nltk.tag import UnigramTagger
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])
from collections import Counter
import string
import re
import nltk
#-------------------------------------------------------------------------

##textf = "There is one handsome boy. The boy has now grown up. He is no longer a allegro now. He is good and hyatt."
#debug mode

#-------------------------------------------------------------------------
def majorfunc(line):

    textf = line;

    numLines = 0
    numSentences = 0
    numWords = 0
    numChars = 0
    numPunc = 0
    numUniqueWords = 0
    numBrand = 0
    numDigits = 0
    numVB = 0
    numNN = 0
    numCC = 0
    numJJ = 0
    numIN = 0
    numDT = 0
    numRB = 0
    numPRP = 0
    numConnect = 0
    numImme = 0
    totNN, totJJ, totIN, totDT, totVB, totRB, totPRP, totCC = 0,0,0,0,0,0,0,0

    brands = {'affinia', 'allegro', 'amalfi', 'ambassador', 'conrad', 'fairmont', 'hardrock', 'hilton', 'homewood', 'hyatt', 'intercontinental', 'james', 'knickerbocker', 'monaco', 'omni', 'palmer', 'sheraton', 'sofitel', 'swissotel', 'talbott'}
    Nouns = {'NN', 'NNS', 'NNP', 'NNPS'}
    Verbs = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}
    Pronouns = {'IN'}
    Prepo = {'PRP', 'PRP$'}
    Conjuncs = {'CC', 'IN'}
    Puncs = {'.','?','!', ',','"','<','>','/','{','}','[',']','|','(',')','@','#','$','%','^','&','*','(',')','-','_','+','=','~','`',':',';'}
    Imme = {'me', 'mine', 'us', 'our', 'ours', 'I', 'mine', 'we'}
    Connect = {'and', 'or', 'else', 'whether', 'eventually', 'however', 'furthermore', 'also', 'subsequently', 'consequently', 'evidently', 'whoever', 'whichever'}
    Adj = {'JJ', 'JJR', 'JJS'}
    Adverbs = {'RB', 'RBR', 'RBS'}
    Deter = {'DT'}
#------------------------------------------------------------------------
    def calcImme(text):
        cnt = 0
        for j in text:
            if(j in Imme):
                cnt += 1
        return cnt
#------------------------------------------------------------------------
    def calcConnect(text):
        cnt = 0
        for j in text:
            if(j in Connect):
                cnt += 1
        return cnt
#------------------------------------------------------------------------
    def tokenizeLine(ln):
        tempwords = nltk.word_tokenize(ln)
        return tempwords
#------------------------------------------------------------------------
    def calcLetters(ln):
        return len(ln) - ln.count(' ')
#------------------------------------------------------------------------
    def calcDigits(ln):
        return len([c for c in ln if c.isdigit()])
#------------------------------------------------------------------------
    def calcPunc(text):
        cnt = 0
        for j in text:
            if(j in Puncs):
                cnt += 1
        return cnt
#------------------------------------------------------------------------
    def calcBrand(text):
        cnt = 0
        for j in text:
            if(j in brands):
                cnt += 1
        return cnt
#------------------------------------------------------------------------
    def calcUniqueWords(ln):
        return len(set(re.findall('\w+', ln.lower())))
#------------------------------------------------------------------------
    def calcPOS(ln):
        POStag = pos_tag(word_tokenize(ln))
        c = Counter([j for i,j in POStag])


        numNN, numJJ, numIN, numDT, numVB, numRB, numPRP, numCC = 0, 0, 0, 0, 0, 0, 0, 0
        for j in c.keys():
            if (j in Nouns):
                numNN += c.get(j)
            if (j in Adj):
                #print("--------------------------------aaaaaaaaaaaaaaaaaaa",j)
                numJJ += c.get(j)
            if (j in Prepo):
                numIN += c.get(j)
            if (j in Deter):
                numDT += c.get(j)
            if (j in Verbs):
                numVB += c.get(j)
            if (j in Adverbs):
                numRB += c.get(j)
            if (j in Pronouns):
                numPRP += c.get(j)
            if (j in Conjuncs):
                numCC += c.get(j)
        #print("numJJ",numJJ)
        return numNN, numJJ, numIN, numDT, numVB, numRB, numPRP, numCC
#------------------------------------------------------------------------
    def calcARI(numChars, numWords, numSentences):
        return ((4.71 * (numChars+1/numWords+1)) + (0.5 * (numWords+1/numSentences+1)) - 21.43)
    
    
    tokenSent = tokenizeLine(line)
    numLines += 1
    numSentences += line.count('.')+ line.count ('!')+ line.count('?') # total num of sentences
    numWords +=  len(tokenSent) # total num of words

    numChars = calcLetters(line)
    numDigits = calcDigits(line)
    numPunc = calcPunc(tokenSent)

    numBrand = calcBrand(tokenSent)
    numImme = calcImme(tokenSent)
    numConnect = calcConnect(tokenSent)
    numUniqueWords = calcUniqueWords(line)

    totNN, totJJ, totIN, totDT, totVB, totRB, totPRP, totCC = 0,0,0,0,0,0,0,0

    totNN, totJJ, totIN, totDT, totVB, totRB, totPRP, totCC = calcPOS(line) # calculate POS tags for each token

    return [(numWords - numPunc),(((numWords - numPunc)+1)/(numSentences+1)), numUniqueWords, ((numImme +1)/(numWords+1)), numBrand, ((numChars+1)/(numWords+1)), numConnect, numDigits,((numVB + 1) /(numNN + 1)), totJJ, totIN, totRB]

