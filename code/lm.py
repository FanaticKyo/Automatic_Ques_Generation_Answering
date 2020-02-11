#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Zimeng Qiu <zimengq@andrew.cmu.edu>

"""
F19 11-411/611 NLP Assignment 3 Task 1
N-gram Language Model Implementation Script
Zimeng Qiu Sep 2019

This is a simple implementation of N-gram language model

Write your own implementation in this file!
"""

import argparse

from utils import *


class LanguageModel(object):
    """
    Base class for all language models
    """
    def __init__(self, corpus, ngram, min_freq, uniform=False):
        """
        Initialize language model
        :param corpus: input text corpus to build LM on
        :param ngram: number of n-gram, e.g. 1, 2, 3, ...
        :param min_freq: minimum frequency threshold to set a word to UNK placeholder
                         set to 1 to not use this threshold
        :param uniform: boolean flag, set to True to indicate this model is a simple uniform LM
                        otherwise will be an N-gram model
        """
        # write your initialize code below
        self.corpus = corpus
        self.ngram = ngram
        self.min_freq = min_freq
        self.uniform = uniform

        #raise NotImplemented

    def build(self):
        """
        Build LM from text corpus
        """
        # Write your own implementation here
        self.unigram = {}
        for i in range(len(self.corpus)):
            for word in self.corpus[i]:
                if word in self.unigram.keys():
                    self.unigram[word]+=1
                else:
                    self.unigram.update({word:1})
            #print("section 1",i,"finished")
                
        min_freq = 5
        small = dict((k, v) for k, v in self.unigram.items() if v < min_freq)

        for j in range(len(self.corpus)):
            for i in small.keys():
                self.corpus[j] = list(map(lambda x: x if x != i else 'UNK', self.corpus[j]))
            #print("section 2",j,"finished")
            
        self.unigram = {}
        for i in range(len(self.corpus)):
            for word in self.corpus[i]:
                if word in self.unigram.keys():
                    self.unigram[word]+=1
                else:
                    self.unigram.update({word:1})
            #print("section 3",i,"finished")
        
        # for i in range(len(train)):
        #     train[i].insert(0," ")
        #     train[i].append(" ")

        self.bigram = {}
        for i in range(len(self.corpus)):
            for j in range(len(self.corpus[i])-1):
                if self.corpus[i][j]+" "+self.corpus[i][j+1] in self.bigram.keys():
                    self.bigram[self.corpus[i][j]+" "+self.corpus[i][j+1]]+=1
                else:
                    self.bigram.update({self.corpus[i][j]+" "+self.corpus[i][j+1]:1})
        
        self.trigram = {}
        for i in range(len(self.corpus)):
            for j in range(len(self.corpus[i])-2):
                if self.corpus[i][j]+" "+self.corpus[i][j+1]+" "+self.corpus[i][j+2] in self.trigram.keys():
                    self.trigram[self.corpus[i][j]+" "+self.corpus[i][j+1]+" "+self.corpus[i][j+2]]+=1
                else:
                    self.trigram.update({self.corpus[i][j]+" "+self.corpus[i][j+1]+" "+self.corpus[i][j+2]:1})

        self.unigram_copy = self.unigram.copy()
        self.uniform_result = {x: 1 for x in self.unigram_copy}          

        #raise NotImplemented

    def most_common_words(self, k):
        """
        This function will only be called after the language model has been built
        Your return should be sorted in descending order of frequency
        Sort according to ascending alphabet order when multiple words have same frequency
        :return: list[tuple(token, freq)] of top k most common tokens
        """
        # Write your own implementation here
        self.build()
        if self.uniform:
            return [tuple((v[0],v[1])) for v in sorted(self.uniform_result.items(), key=lambda kv: (-kv[1], kv[0]))][:k]
        elif self.ngram == 2:
            return [tuple((v[0],v[1])) for v in sorted(self.bigram.items(), key=lambda kv: (-kv[1], kv[0]))][:k]
        elif self.ngram == 3:
            return [tuple((v[0],v[1])) for v in sorted(self.trigram.items(), key=lambda kv: (-kv[1], kv[0]))][:k]
        else:
            return [tuple((v[0],v[1])) for v in sorted(self.unigram.items(), key=lambda kv: (-kv[1], kv[0]))][:k]

        #raise NotImplemented


def calculate_perplexity(models, coefs, data):
    """
    Calculate perplexity with given model
    :param models: language models
    :param coefs: coefficients
    :param data: test data
    :return: perplexity
    """
    # Write your own implementation here
    import math 
    for i in range(len(models)):
        models[i].build()
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] not in models[0].unigram.keys():
                data[i][j] = "UNK"

    count_training = 0
    for i in range(len(models[0].corpus)):
        count_training += len(models[0].corpus[i])
    
    count = 0
    for i in range(len(data)):
        count += len(data[i])
    sum_prop = 0
    for i in range(len(data)):
        for j in range(2,len(data[i])):
            prop = 0
            prop1 = 1/len(models[0].uniform_result)
            prop2 = models[0].unigram[data[i][j]]/count_training

            if data[i][j-1]+" "+data[i][j] in models[0].bigram.keys():
                prop3 = (models[0].bigram[data[i][j-1]+" "+data[i][j]])/models[0].unigram[data[i][j-1]]
            else:
                prop3 = (1/(models[0].unigram[data[i][j-1]]+len(models[0].uniform_result)))

            if (data[i][j-2] + " " + data[i][j-1]+" "+data[i][j] in models[0].trigram.keys()): 
                prop4 = (models[0].trigram[data[i][j-2] + " " + data[i][j-1]+" "+data[i][j]]+1)/models[0].bigram[data[i][j-2] + " " + data[i][j-1]]           
            elif  (data[i][j-2] + " " + data[i][j-1]+" "+data[i][j] not in models[0].trigram.keys()) and (data[i][j-2] + " " + data[i][j-1] in models[0].bigram.keys()):
                prop4 = (1/models[0].bigram[data[i][j-2] + " " + data[i][j-1]])                         
            else:
                prop4 = (models[0].unigram[data[i][j]]/count_training)
                

            
            if coefs[0]>0:           
                prop += prop1*coefs[0]
                
            if coefs[1]>0:           
                prop += prop2*coefs[1]
                
            if coefs[2]>0:           
                prop += prop3*coefs[2]
                
            if coefs[3]>0:           
                prop += prop4*coefs[3]
                
            sum_prop += math.log2(prop)
    return 2**(sum_prop/(-count))



    

# Do not modify this function!
def parse_args():
    """
    Parse input positional arguments from command line
    :return: args - parsed arguments
    """
    parser = argparse.ArgumentParser('N-gram Language Model')
    parser.add_argument('coef_unif', help='coefficient for the uniform model.', type=float)
    parser.add_argument('coef_uni', help='coefficient for the unigram model.', type=float)
    parser.add_argument('coef_bi', help='coefficient for the bigram model.', type=float)
    parser.add_argument('coef_tri', help='coefficient for the trigram model.', type=float)
    parser.add_argument('min_freq', type=int,
                        help='minimum frequency threshold for substitute '
                             'with UNK token, set to 1 for not use this threshold')
    parser.add_argument('testfile', help='test text file.')
    parser.add_argument('trainfile', help='training text file.', nargs='+')
    args = parser.parse_args()
    return args


# Main executable script provided for your convenience
# Not executed on autograder, so do what you want
if __name__ == '__main__':
    # parse arguments
    args = parse_args()

    # load and preprocess train and test data
    train = preprocess(load_dataset(args.trainfile))
    test = preprocess(read_file(args.testfile))

    # build language models
    uniform = LanguageModel(train, ngram=1, min_freq=args.min_freq, uniform=True)
    unigram = LanguageModel(train, ngram=1, min_freq=args.min_freq)
    bigram = LanguageModel(train, ngram=2, min_freq=args.min_freq)
    trigram = LanguageModel(train, ngram=3, min_freq=args.min_freq)

    # calculate perplexity on test file
    ppl = calculate_perplexity(
        models=[uniform, unigram, bigram, trigram],
        coefs=[args.coef_unif, args.coef_uni, args.coef_bi, args.coef_tri],
        data=test)

    print("Perplexity: {}".format(ppl))





