# LING 573 Question Answering System
# Code last updated 4/11/14 by Claire Jaja
# This code implements an Answer Processor for the question answering system.

class AnswerProcessor:
    def __init__(self,passages,answer_template):
        self.passages = passages
        self.answer_template = answer_template

    # a method to extract possible answers from the passages and rank them
    def extract_answers(self):
        # will probably want to loop through passages, count n-grams
        # also increment scores based on something like inverse passage rank
        pass

    # a method to check candidate answers against the answer template
    def filter_answers(self):
        # do some checking here
        pass

class CandidateAnswer:
    def __init__(self,answer):
        self.answer = answer
        self.score = 0

    def set_score(self,score):
        self.score = score
