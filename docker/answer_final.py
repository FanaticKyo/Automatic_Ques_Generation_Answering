import nltk
import spacy
from nltk.stem.snowball import SnowballStemmer
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer
import numpy as np
import re
import sys, io
import ranking
import copy
from fuzzywuzzy import fuzz
import answer_wh


parse = nltk.CoreNLPParser(url = "http://localhost:9090")
wh_words = set(['why', 'which', 'whose', 'who', 'whom', 'where', 'when', 'what','how'])

#change to large?
en_nlp = spacy.load('en_core_web_sm')

parse = nltk.CoreNLPParser(url = "http://localhost:9000")
wh_words = set(['why', 'which', 'whose', 'who', 'whom', 'where', 'when', 'what','how'])

#input: a list of sentences
#return: a list of nltk trees, with root node removed
def get_nlp_tree(sentences):
    lst = []
    for s in sentences:
        s_parse_tree = parse.raw_parse(s)
        for subtree in s_parse_tree:
            lst.append(subtree[0])
    return lst



def q_type(q_tree):
    label = 'OTHERS'
    q_word = "OTHERS"
    words = q_tree.leaves()
    if q_tree.label() == "SBARQ":
        label = "WH"
        q_word = get_wh_word(words)
        binary_form = q_tree.leaves()[1:]
        transformed = bin_form(label,binary_form)
    elif q_tree.label() == "SQ":
        label = "BINARY"
        q_word = "BINARY"
        binary_form = q_tree.leaves()
        transformed = bin_form(label,binary_form)
    else:
        transformed = " ".join(words)
    return (q_word, transformed)

def get_wh_word(words):
    for i in range(len(words)):
        w = words[i].lower()
        if w in wh_words:
            if w == "how":
                if i+1<len(words) and (words[i+1]).lower() == "many":
                    return "how_many"
                return "how"
            if w in ['who','whom']:
                return 'who'
            return w
    return None




def traverse_tree(tree,lst):
    for subtree in tree:
        if type(subtree) == nltk.tree.Tree:
            traverse_tree(subtree,lst)
        else:
            lst.append(subtree)

def get_leaves(tree):
    res = []
    if isinstance(tree,list):
        for subtree in tree:
            traverse_tree(subtree,res)
        return res
    if type(tree) == nltk.tree.Tree:
        return tree.leaves()

    
    

def bin_form(label,binary_form):
    question = ' '.join(binary_form)
    tree = get_nlp_tree([question])[0]
 

    if type(tree[0]) == nltk.tree.Tree:
        front = tree[0].leaves()
    else:
        front = get_leaves(tree[0])

    back = get_leaves(tree[1:])


    if len(front) >1:
        doc = en_nlp(' '.join(front))
        do_deletion = False
        for n in doc:
            if n.lemma_.lower() in ['be', 'do']:
                do_deletion == True
                break
        if do_deletion:
            front = front[1:]
        else:
            front = front[1:] + [front[0].lower()]
    else:
        front = []
    if isinstance(back,list):
        res = front + back
    else:
        res = front + [back]
    if label == "WH":
        return ' '.join(res[:len(res)-2])
    return ' '.join(res[:len(res)-1])

 






article_filename = sys.argv[1]
questions_filename = sys.argv[2]

#article_filename = 'test_doc.txt'
#questions_filename = 'q_test.txt'
with io.open(article_filename, 'r', encoding='utf8') as f:
    text = f.read()
with io.open(questions_filename, 'r', encoding='utf8') as f:
    questions = f.read()
    questions = questions.split('\n')

text = text.split('\n')
text = list(filter(lambda x: len(x.split()) >3,text))

text = ' '.join(text)
blob = TextBlob(text)
sentences = [item.raw for item in blob.sentences]

#process questions
q_trees = get_nlp_tree(questions)
fuzzy_lst = []
wh_q_lst = []
labels = []
processed_q_lst = []
for tree in q_trees:
    (wh_word, binary_form) = q_type(tree)
    #print(wh_word, 'bin form:',binary_form)
    if wh_word == "BINARY" or wh_word == "OTHERS":
        fuzzy_lst.append(binary_form)
    else:
        wh_q_lst.append(binary_form)
    processed_q_lst.append(binary_form)
    labels.append(wh_word)



# get the best guess sentence
fuzzy_ans = []
predictions = ranking.fuzzyCompare(sentences,fuzzy_lst)
threshold = 89
for (best_sentence, score) in predictions:
    if score< threshold:
        fuzzy_ans.append("No.")
    else:
        fuzzy_ans.append("Yes.")

wh_guess = []
ind = ranking.ranking(sentences,wh_q_lst)
for i in ind:
    wh_guess.append(sentences[i])
######################


#combine all candidates
ind_wh = 0
ind_binary = 0
candidates= []
for lab in labels:
    if lab != "BINARY" and lab != "OTHERS":
        candidates.append(wh_guess[ind_wh])
        ind_wh +=1
    else:
        candidates.append(fuzzy_ans[ind_binary])
        ind_binary+=1

#################
anser_lst = []
for i in range(len(labels)):
    wh_word = labels[i]
    if wh_word != "BINARY" and wh_word != "OTHERS":
        wh_question = getattr(answer_wh, 'answer_' + wh_word)
        a = wh_question(processed_q_lst[i], candidates[i])
        anser_lst.append(a)
    else:
        anser_lst.append(candidates[i])


final_ans = ''
for ans in anser_lst:
    final_ans+=ans +'\n'

print(final_ans)



'''
#if not using the answer_wh:
count_binary = 0
count_wh = 0
final_ans = ''
for lab in labels:
    if lab == "BINARY" or lab == "OTHERS":
        final_ans += fuzzy_ans[count_binary]+'\n'
        count_binary+=1
    else:
        final_ans += wh_guess[count_wh] + '\n'
        count_wh+=1
print(final_ans)
'''



