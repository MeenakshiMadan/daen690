import nltk
import nltk.classify.util
import os
#import re
import io
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
import multiprocessing as mp

#file locations to be changed as necessary

#store all positive classified training text here
pos_file_dir = "txt_sentoken/pos/"
#store all negative classified training text here
neg_file_dir = "txt_sentoken/neg/"
#store list of headlines here
headline_dir = "headlines/"
#output file name
output_file = "output.csv"

#sentence tokenizer that removes stopwords
def format_sentence(sent):
    token_words = nltk.word_tokenize(sent)
    for w in token_words:
        if w in stopwords.words("english"):
            token_words.remove(w)
    return({word: True for word in token_words})

#training set makers (used with nb_trainer)
def pos_training_set_maker(review):
    with open(pos_file_dir + review, encoding="utf8") as f:
        line = f.read()
        for l in line.split():
            return [format_sentence(l), 'pos']

def neg_training_set_maker(review):
    with open(neg_file_dir + review, encoding="utf8") as f:
        line = f.read()
        for l in line.split():
            return [format_sentence(l), 'neg']

#multiprocessing based method for training the NaiveBayesClassifier
#training data retrieved from
#http://ai.stanford.edu/~amaas/data/sentiment/

def nb_trainer():

    #store training data in the below folders
    pos_review_list = os.listdir(pos_file_dir)
    neg_review_list = os.listdir(neg_file_dir)

    #adjust pool to number of processes your system can handle
    pool = mp.Pool(processes=16)

    poscorpus = [pool.apply(pos_training_set_maker, args=(x,)) for x in pos_review_list]
    negcorpus = [pool.apply(neg_training_set_maker, args=(x,)) for x in neg_review_list]

    training = poscorpus + negcorpus

    classifier = NaiveBayesClassifier.train(training)
    return classifier


#method classifying a single headline
def process_headline(filepath, classifier):
    processed = []
    #headlines = []
    with open(filepath, encoding="utf8") as f:
        line = f.read()
        headlines = line.splitlines()
    for headline in headlines:
        probabilities = classifier.prob_classify(format_sentence(headline))
        processed.append([headline,probabilities.max(),probabilities.prob("pos"),probabilities.prob("neg")])
    return processed

#parallel processer for headlines
def read_headlines(filedir,classifier):
    headlines_list = os.listdir(filedir)

    #adjust pool to number of processes your system can handle
    pool = mp.Pool(processes=8)

    classed_text = [pool.apply(process_headline, args=(filedir+x,classifier,)) for x in headlines_list]
    return classed_text



def main():

    classifier = nb_trainer()
    classifier.show_most_informative_features()
    f = open(output_file,"w")
    for x in read_headlines(headline_dir,classifier):
        for y in x:
            formatted_line = ""
            for c in y:
                formatted_line += str(c) + ','
            f.write(formatted_line[:-1] + '\n')

if __name__ == '__main__':
    main()
