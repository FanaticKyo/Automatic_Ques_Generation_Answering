
import nltk
from sklearn.metrics.pairwise import cosine_similarity
import spacy
from nltk.stem.snowball import SnowballStemmer
#from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
import numpy as np
import re

from contextlib import contextmanager
import sys, os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout


nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

stopwords = nltk.corpus.stopwords.words('english')
stemmer = SnowballStemmer("english")
en_nlp = spacy.load('en_core_web_sm')

# tokenization and stemming
# assuming the text is an original sentence, return the stemming of the tokens
def tokenization_and_stemming(text):
    # exclude stop words and tokenize the document, generate a list of string 
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent) if word not in stopwords]
    filtered_tokens = []
    
    
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)        
    # stemming
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

# tokenization without stemming
def tokenization(text):
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent) if word not in stopwords]
    filtered_tokens = []
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens

# perform ranking of cosine similarity of tfidf vectorization
# return: 1D numpy array of shape 1 x len(questions), each element is the index of top ranked candidate answer
def ranking(candidates, questions):
	# use TfidfVectorizer to create tf-idf matrix
	# max_df : maximum document frequency for the given word
	# min_df : minimum document frequency for the given word
	# max_features: maximum number of words
	# use_idf: if not true, we only calculate tf
	# stop_words : built-in stop words
	# tokenizer: how to tokenize the document
	# ngram_range: (min_value, max_value), eg. (1, 3) means the result will include 1-gram, 2-gram, 3-gram
	tfidf_model = TfidfVectorizer(max_df=0.8, max_features=2000,
	                                 min_df=0, 
	                                 use_idf=True, tokenizer=tokenization_and_stemming, ngram_range=(1,3))
	q_starting_ind = len(candidates)
	candidates.extend(questions)
	tfidf_matrix = tfidf_model.fit_transform(candidates)
	cos_matrix = cosine_similarity(tfidf_matrix)
	cos_matrix[cos_matrix >=1] = 0
	ind = cos_matrix[q_starting_ind:,:q_starting_ind].argmax(axis = 1)
	return ind




def fuzzyCompare(candidates,questions):
    res = []
    for q in questions:
        guess = process.extractOne(q, candidates,scorer = fuzz.partial_ratio)
        res.append(guess)
    return res






