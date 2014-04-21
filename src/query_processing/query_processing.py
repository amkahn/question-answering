# LING 573 Question Answering System
# Code last updated 4/15/14 by Andrea Kahn
#
# This code implements a QueryProcessor for the question answering system.


import sys
import nltk
from general_classes import *

# TODO: A QueryProcessor should be initialized with the Question object, but should it
# have this question as an attribute, or should it have attributes id, type, q, target that
# match those of the question?
# Advantage of first approach: allows us to change the Question and have the QueryProcessor
# update automatically (not sure we'd ever do this).
# Advantage of second approach: saves typing (access the id with self.id, versus self.question.id).

# A QueryProcessor object has the attribute "question", a Question object.

class QueryProcessor(object):
    def __init__(self, question):
        self.question = question

	# This method returns a set of SearchQuery objects.
    def generate_queries(self):
        tokenized_q = nltk.word_tokenize(self.question.q)
        tokenized_target = nltk.word_tokenize(self.question.target)
		# FIXME: Strip out punctuation tokens (here is a temporary fix)
        punctuation = ['?','.',',']
        query_terms = filter(lambda x: x not in punctuation, tokenized_q + tokenized_target)
        query_dict = {}
        
        # NB: For now, the weights of the search terms are equal to the counts of the term
        # in the question plus the target.
        for term in query_terms:
            if query_dict.get(term) == None:
                query_dict[term] = 1
            else:
                query_dict[term] += 1

        query = SearchQuery(query_dict, 1)
#       sys.stderr.write("DEBUG  Here is the search query: %s\n" % query.to_string())

		# FIXME: Issue with leading escape character in some questions 
        return [query]
	
	# This method returns an AnswerTemplate object.
    def generate_ans_template(self):
	
		# NB: The following if statement should always evaluate as True in our system, but
		# its inclusion enables the system to more easily be extended to handle other types
		# of questions, for which the text-processing and AnswerTemplate-generation steps
		# might be slightlydifferent.

        if self.question.type=="FACTOID":		
			# do some sort of text-processing on the natural-language question and context
			# to determine NE type
			# generate a corresponding AnswerTemplate object
			# return it
            return None

        else:
            sys.stderr.write("Warning: System can only handle \"factoid\" questions\n")
