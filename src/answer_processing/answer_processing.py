# LING 573 Question Answering System
# Code last updated 4/22/14 by Claire Jaja
# This code implements an Answer Processor for the question answering system.

from general_classes import AnswerTemplate, Passage
from operator import itemgetter, attrgetter
from collections import Counter, defaultdict
import nltk
import sys
from bs4 import BeautifulSoup

class AnswerProcessor:
    def __init__(self,passages,answer_template,stopword_list=[]):
        self.passages = passages
        self.answer_template = answer_template
        self.ranked_answers = []
        self.stopword_list = stopword_list

#    def generate_and_rank_answers_old(self):
#        # get answers from the passages
#        self.extract_answers()
#        # reweight answers based on answer template
#        self.reweight_answers()           
#        # sort answers by score
#        self.rank_answers()
#        # return top 20 highest ranked answers
#        return self.ranked_answers[:20]

    def generate_and_rank_answers(self):
        # get answers from the passages
        self.extract_answers()
        # remove answers with query words
        self.remove_query_words()
        # combine answer weights
        self.combine_answers()
        # reweight answers based on answer template
        self.reweight_answers()           
        # sort answers by score
        self.rank_answers()
        # return top 20 highest ranked answers
        if len(self.ranked_answers) >= 20:
            return self.ranked_answers[:20]
        else:
            return self.ranked_answers

    # a method to extract possible answers from the passages and rank them
#    def extract_answers_old(self):
#        # for now, just take the first 250 characters of the passage as the answer
#        for passage in self.passages:
#            answer_candidate = AnswerCandidate(passage.passage[:250],passage.doc_id)
#            answer_candidate.set_score(passage.weight)
#            self.ranked_answers.append(answer_candidate)

    def extract_answers(self):
        # here's a possible clever answer extractor
        answer_docs = defaultdict(set)
        answer_score = defaultdict(lambda:0)
        self.unigram_answers = []
        for passage in self.passages:
            passage_list = nltk.word_tokenize(passage.passage)
            #sys.stderr.write("Tokenized passage is"+str(passage_list)+"\n")
            for i in range(len(passage_list)):
                answers = []
                # unigram
                answers.append(passage_list[i])
                if i < len(passage_list) - 1: # can do bigrams
                    answers.append(" ".join(passage_list[i:i+2]))
                    if i < len(passage_list) - 2: # can do trigrams
                        answers.append(" ".join(passage_list[i:i+3]))
                        if i < len(passage_list) - 3: # can do 4-grams
                            answers.append(" ".join(passage_list[i:i+4]))
                for answer in answers:
                    answer_docs[answer].add(passage.doc_id)
                    # passage weight is negative - closer to 0 is better
                    # change to positive, then take inverse
                    # higher score is still better, but now will be all positive
                    answer_score[answer] += (-passage.weight)**-1
       # then find answers with highest score?
        for answer,score in answer_score.iteritems():
            if len(answer.split()) == 1:
                self.unigram_answers.append((answer,score))
            # initialize answer candidate with answer and random doc ID from doc IDs it occured in
            ac = AnswerCandidate(answer,next(iter(answer_docs[answer])))
            ac.set_score(score)
            self.ranked_answers.append(ac)

    # remove words from original question and stop words
    def remove_query_words(self):
        # go through answers
        for i in xrange(len(self.ranked_answers)-1,-1,-1):
            answer = self.ranked_answers[i]
            for word in answer.answer.split():
                # if any word in the answer is in the list of query terms
                punctuation = [':',"'","''",'(',')','&',';','_','.','!','?',',']
                if word.lower() in self.answer_template.query_terms or word.lower() in self.stopword_list or word in punctuation:
                    # remove that answer
                    del self.ranked_answers[i]
                    break
            else:
                continue

    # combine answer candidates so that unigrams aren't highest
    def combine_answers(self):
        # update score of each answer
        # to be current score + sum of scores of answer unigrams in it
        for answer in self.ranked_answers:
            if len(answer.answer.split()) > 1: # only update non-unigram scores
                new_score = answer.score
                for unigram_answer,score in self.unigram_answers:
                        if unigram_answer in answer.answer:
                            new_score += score
                answer.set_score(new_score) 

    # a method to check candidate answers against the answer template
    def reweight_answers(self):
        for answer_candidate in self.ranked_answers:
            # find NEs and types
            for NE_type,weight in self.answer_template.type_weights.iteritems():
                # if this NE type is in the answer_candidate
                # set the score to the previous score times the type's weight
                # for now, assume all NE types in all answer candidates
                new_score = answer_candidate.score*weight
                answer_candidate.set_score(new_score)

    def rank_answers(self):
        self.ranked_answers.sort(reverse=True,key=attrgetter('score'))


class AnswerCandidate:
    def __init__(self,answer,doc_id):
        self.answer = answer
        self.doc_id = doc_id
        self.score = 0

    def set_score(self,score):
        self.score = score

    def __repr__(self):
        return "'%s' from %s with score %s" % (self.answer, self.doc_id, self.score)
