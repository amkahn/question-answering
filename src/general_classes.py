# LING 573 Question Answering System
# Code last updated 4/11/14 by Claire Jaja
# This code holds classes that need to be accessed by various parts of the system.

class AnswerTemplate:
    def __init__(self,question):
        self.original_question = question
        # should the AnswerTemplate get the question and then generate the template from that?
        # or should the QueryProcessor generate the pieces and then pass them to the AnswerTemplate?

    # one possibility - AnswerTemplate generates the template
    def generate_template(self):
        # do something here to figure out NE type
        # or alternatively, gather probabilities for all different NE types
        pass
