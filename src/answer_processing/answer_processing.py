# LING 573 Question Answering System
# Code last updated 4/18/14 by Claire Jaja
# This code implements an Answer Processor for the question answering system.

from general_classes import AnswerTemplate, Passage
import operator

class AnswerProcessor:
    def __init__(self,passages,answer_template):
        self.passages = passages
        self.answer_template = answer_template
        self.ranked_answers = []

    def generate_and_rank_answers(self):
        # get answers from the passages
        self.extract_answers()
        # reweight answers based on answer template
        self.reweight_answers()           
        # sort answers by score
        self.rank_answers()
        return self.ranked_answers

    # a method to extract possible answers from the passages and rank them
    def extract_answers(self):
        # for now, just take the entire text of the passage as the answer
        for passage in self.passages:
            answer_candidate = AnswerCandidate(passage.passage,passage.doc_id)
            answer_candidate.set_score(passage.weight)
            self.ranked_answers.append(answer_candidate)
            # later, do something more clever, like count n-grams
            # also increment scores based on something like inverse passage rank

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
        self.ranked_answers.sort(key=operator.attrgetter('score'))


class AnswerCandidate:
    def __init__(self,answer,doc_id):
        self.answer = answer
        self.doc_id = doc_id
        self.score = 0

    def set_score(self,score):
        self.score = score
