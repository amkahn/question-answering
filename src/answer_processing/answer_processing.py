# LING 573 Question Answering System
# Code last updated 4/22/14 by Claire Jaja
# This code implements an Answer Processor for the question answering system.

from general_classes import AnswerTemplate, Passage
from operator import itemgetter, attrgetter
from collections import Counter, defaultdict
import nltk
import sys
import re


class AnswerProcessor:
    def __init__(self,passages,answer_template,stopword_list,parameters):
        self.parameters = parameters
        self.passages = passages
        self.answer_template = answer_template
        self.ranked_answers = []
        self.stopword_list = stopword_list
        self.stopword_list |= {"'m","'s","n't","ca","wo","did"}
        #self.punctuation = {':',"'","''",'(',')','&',';','_','.','!','?',',','-','--','...','`','``'}
        #for passage in self.passages:
        #    sys.stderr.write("PASSAGE: "+passage.passage+"\n")

    def generate_and_rank_answers(self):
        # get answers from the passages
        self.extract_answers()
        # filter answers
        self.filter_answers()
        # combine answer weights
        self.combine_answers()
        # reweight answers based on answer template
        self.reweight_answers()
        # sort answers by score
        self.rank_answers()

        # top 20 passages
        # and their doc IDS
        passages_to_return = []
        doc_ids_to_return = []
        i = 0
        while len(passages_to_return) < 20 and i < len(self.ranked_answers):
            answer = self.ranked_answers[i]

            # do something to get best passage(s)

            # create a list of (doc_id,passage_list) tuples
            possible_passages = answer.doc_ids.items()
            # sort so that documents with most passages are first
            possible_passages.sort(key=lambda x:len(x[1]), reverse=True)

            # return up to the parameter for passages per answer candidate
            for j in range(int(self.parameters['passages_per_answer_candidate'])):
                # question: return multiple passages per document ID within answer candidate?
                # probably don't want to do that
                # for now, within particular answer candidate, will return one passage per document ID

                # as long as there are passages left to return
                if j < len(possible_passages):
                    # grab the document id and passage list
                    doc_id,passages = possible_passages[j]
                    # check that I haven't already returned maximum number of passages for this doc ID
                    if doc_ids_to_return.count(doc_id) < int(self.parameters['passages_per_doc_id']):
                        # use the first passage in the list
                        passage = passages[0]
                        # truncate to 250 characters centered on answer
                        answer_index = passage.find(answer.answer)
                        passage_start = answer_index - (250-len(answer.answer))/2
                        if passage_start < 0:
                            passage_start = 0
                        passage = passage[passage_start:passage_start+250]
                        # check that I'm not already returning the same exact passage
                        if passage not in passages_to_return:
                            passages_to_return.append(passage)
                            doc_ids_to_return.append(doc_id)

            i += 1

        # combine doc_ids and passages in one list
        to_return = zip(doc_ids_to_return,passages_to_return)
        # add question id
        to_return = [[self.answer_template.question_id]+list(x) for x in to_return]
        if len(to_return) >= 20:
            return to_return[:20]
        else:
            return to_return

    def extract_answers(self):
        # here's a possible clever answer extractor
        answer_docs = defaultdict(lambda:defaultdict(list))
        answer_score = defaultdict(lambda:0)
        number_passages = Counter()
        self.unigram_answers = []
        for passage in self.passages:
            sentences = []
            split_passage = passage.passage.split("...")
            for x in split_passage:
                sentences.extend(nltk.sent_tokenize(x))
            passage_list = [nltk.word_tokenize(t) for t in sentences]
            #sys.stderr.write("Tokenized passage is"+str(passage_list)+"\n")
            for sentence in passage_list:
                for i in range(len(sentence)):
                    # up to 4-grams
                    for j in range(4):
                        if i < len(sentence) - j:
                            answer_score[" ".join(sentence[i:i+j+1])] += passage.weight
                            if passage.doc_id:
                                number_passages[" ".join(sentence[i:i+j+1])] += 1
                                answer_docs[" ".join(sentence[i:i+j+1])][passage.doc_id].append(passage.passage)
                            else:
                                number_passages[" ".join(sentence[i:i+j+1])] += int(self.parameters['snippet_passage_count'])

       # then find answers with highest score?
        for answer,score in answer_score.iteritems():
            if len(answer.split()) == 1 and not re.search(r'^\W$',answer):
                self.unigram_answers.append((answer,score))
            # initialize answer candidate with answer and the doc IDs where it occured in
            ac = AnswerCandidate(self.answer_template.question_id,answer,answer_docs[answer])
            ac.number_passages = number_passages[answer]
            ac.set_score(score)
            self.ranked_answers.append(ac)

    # remove answers with words from original query or "..." starting/ending with punctuation or stop word
    def filter_answers(self):
        # some regexes for comparisons
        stopword_re = re.compile("|".join(["^"+re.escape(x) for x in self.stopword_list]+[re.escape(x)+"$" for x in self.stopword_list]),re.IGNORECASE)
        punctuation_re = re.compile(r'^\W|\W$')
        query_terms_re = re.compile("|".join(re.escape(x) for x in self.answer_template.query_terms),re.IGNORECASE)

        # go through answers
        for i in xrange(len(self.ranked_answers)-1,-1,-1):
            answer = self.ranked_answers[i]
            answer_words = answer.answer.split()

            # remove answers if not in at least one document
            # try different number of documents to see
            if len(answer.doc_ids) < int(self.parameters['num_docs']):
                #sys.stderr.write("Deleting - doesn't occur in any AQUAINT doc.\n")
                del self.ranked_answers[i]
            elif answer.number_passages < int(self.parameters['num_passages']):
                #sys.stderr.write("Deleting - doesn't occur in at least "+self.parameters['num_passages']+" passages.\n")
                del self.ranked_answers[i]

            # remove answer if starts or ends with stopword or punctuation
            # or if it contains any of query terms
            elif stopword_re.search(answer.answer) or punctuation_re.search(answer.answer) or query_terms_re.search(answer.answer):
                del self.ranked_answers[i]


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
        # find NEs and types
        # person, organization, object, location, time_ex, number, other

        # for now, person, organization, and location share one regex
        # just checking if it starts with capital letter
        pers_org_loc_re = re.compile(r'^[A-Z]')

        # time expressions
        months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sept","Oct","Nov","Dec"]
        date = [r"^([0-9]{1,2} ?(-|/) ?)?([0-9]{1,2} ?(-|/) ?)?[0-9]{2,4}$"]
        time_ex_re = re.compile("|".join(months+date))

        # numbers
        number_words = ["one","two","three","four","five","six","seven","eight","nine","ten",
"eleven","twelve","thirteen","fifteen","twenty","thirty","forty","fifty","hundred","thousand","million","billion"]
        number_re = re.compile("|".join(number_words+["[0-9]"]))

        # for now, don't capture objects (think about how to do this...)
        # so everything else will be considered other

        for answer_candidate in self.ranked_answers:
            # if person, organization, or location
            # find which category has highest weight in answer template
            # and upweight accordingly
            if pers_org_loc_re.search(answer_candidate.answer):
                weights = []
                weights.append(self.answer_template.type_weights['person'])
                weights.append(self.answer_template.type_weights['organization'])
                weights.append(self.answer_template.type_weights['location'])
                weights.sort(reverse=True)
                new_score = answer_candidate.score*weights[0]
            # if time expression, upweight by that
            elif time_ex_re.search(answer_candidate.answer):
                new_score = answer_candidate.score*self.answer_template.type_weights['time_ex']
            # if number, upweight by that
            elif number_re.search(answer_candidate.answer):
                new_score = answer_candidate.score*self.answer_template.type_weights['number']
            # else, upweight by other
            else:
                new_score = answer_candidate.score*self.answer_template.type_weights['other']

            answer_candidate.set_score(new_score)


    def rank_answers(self):
        self.ranked_answers.sort(reverse=True,key=attrgetter('score'))
        # final step, remove answers that are substring of any other answer
        to_remove = set()
        for i in range(len(self.ranked_answers)-1,-1,-1):
            answer = self.ranked_answers[i]
            for j in range(i-1,-1,-1):
                other_answer = self.ranked_answers[j]
                if answer.answer in other_answer.answer:
                    to_remove.add(i)
        to_remove = sorted(list(to_remove),reverse=True)
        for i in to_remove:
            del self.ranked_answers[i]


class AnswerCandidate:
    def __init__(self,question_id,answer,doc_ids):
        self.question_id = question_id
        self.answer = answer
        self.doc_ids = doc_ids
        self.score = 0
        self.number_passages = 0

    def set_score(self,score):
        self.score = score

    def __repr__(self):
        return "'%s' from %s with score %s" % (self.answer, self.doc_id, self.score)
