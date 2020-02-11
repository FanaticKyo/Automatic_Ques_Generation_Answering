import sys
import io
#from nltk.tree import Tree
from textblob import TextBlob
import spacy

def find_sentences_with_attr(attrs, question, sentence): 
    #nlp = spacy.load('en_trf_xlnetbasecased_lg')
    nlp = spacy.load('en_core_web_sm')
    target_token = []
    sentence = nlp(sentence)
    for token in sentence.ents:
        if token.label_ in attrs and token.text not in question: 
            target_token.append(token.text)
    #target_token = nlp(' '.join(target_token))
    #return target_token
    return ' '.join(target_token)


def answer_where(question, article): 
    # Step 1: find candidate sentences in article by NER tags 
    where_attrs = ['NORP','FAC','GPE','LOC','ORG']
    candidate = find_sentences_with_attr(where_attrs, question, article)
    # Step 2: if failed: pattern match using in/at
    if len(candidate) == 0: # if receiving no result from last step 
        for sub_sentence in article.split(','):
            if 'in' in sub_sentence: 
                idx = sub_sentence.index('in')
                candidate = sub_sentence[idx:]
            elif 'at' in sub_sentence: 
                idx = sub_sentence.index('at')
                candidate = sub_sentence[idx:]
    #nlp = spacy.load('en_trf_xlnetbasecased_lg')
    nlp = spacy.load('en_core_web_sm')
    #candidate = nlp(' '.join(candidate))
    #return candidate
    
    return (candidate)

def answer_which(question, article):
    which_attrs = ['LANGUAGE']
    candidates = find_sentences_with_attr(which_attrs, question, article)
    #nlp = spacy.load('en_trf_xlnetbasecased_lg')
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(question)
    if len(candidates) == 0: 
        candidates = []
        for token in doc: 
            if token.pos_ == 'NOUN': 
                if (('not' in question and 'not' in article) or 
                ('not' not in question and 'not' not in article)) and token.text in article: 
                    candidates.append(token.text)
                elif (('not' in question and 'not' not in article) or 
                ('not' not in question and 'not' in article)) and token.text not in article:
                    candidates.append(token.text)  
    return ' '.join(candidates)

def answer_when(question, article):
    when_attrs = ['DATE','TIME']
    candidate_sentences = find_sentences_with_attr(when_attrs, question, article)
    return candidate_sentences


def answer_what(question, article):
    #nlp = spacy.load('en_trf_xlnetbasecased_lg')
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(article)
    punct_idx = -1 
    root_idx = 0 
    for i, word in enumerate(doc):
        if word.dep_ == 'ROOT': 
            root_idx = i 
        if word.dep_ == 'punct' and root_idx == 0: punct_idx = i
    sub_sentence = doc[punct_idx+1:root_idx]
    subj_idx = 0 
    punct_idx = -1 
    for j, word in enumerate(sub_sentence):
        if 'nsubj' in word.dep_: 
            subj_idx = j 
        if word.dep_ == 'punct' and subj_idx == 0: punct_idx = j 
    candidate = sub_sentence[punct_idx+1:subj_idx+1]
    return str(candidate)

def answer_who(question, article):
    who_attrs = ['PERSON', 'NORP']
    candidates = find_sentences_with_attr(who_attrs, question, article)
    return candidates

def answer_how(question, article):
    how_attrs = []
    candidate_sentences = find_sentences_with_attr(how_attrs, question, article)
    return candidate_sentences

def answer_how_much(question, article):
    how_much_attrs = ['PERCENT', 'MONEY', 'QUANTITY']
    candidate_sentences = find_sentences_with_attr(how_much_attrs, question, article)
    return candidate_sentences

def answer_why(question, sentence): 
    if "because" in sentence.lower(): 
        sentence = "Because" + sentence.split('because')[1].rstrip(',') + '.'
    if "due to" in sentence.lower():
        print("sentence.split('due to')[1]",sentence.lower().split('due to'))
        sentence = "Because of" + sentence.lower().split('due to')[1].rstrip(',') + '.'
    if "thanks to" in sentence.lower(): 
        sentence = "Thanks to" + sentence.split('thanks to')[1].rstrip(',') + '.'
    #nlp = spacy.load('en_trf_xlnetbasecased_lg')
    nlp = spacy.load('en_core_web_sm')
    #sentence = nlp(sentence)
    return sentence

def answer_how_many(question, sentence): 
    #nlp = spacy.load('en_trf_xlnetbasecased_lg')
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)
    candidate = []
    for token in doc: 
        if token.dep_ == 'nummod': 
            candidate.append(token.text)
    #candidate = nlp(' '.join(candidate))
    #return candidate
    return ' '.join(candidate)

def answer_other(question, article): 
    return article

