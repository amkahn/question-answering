# LING 573 Question Answering System
# Code last updated 4/22/14 by Andrea Kahn
#
# This code implements a QueryProcessor for the question answering system.


import sys
import nltk
import re
from general_classes import *


# A QueryProcessor object has the attribute "question", a Question object.

class QueryProcessor(object):

    def __init__(self, question):
        self.question = question
        self.query_voc = self.generate_voc()


    # This method returns a dictionary of unigrams appearing in the original question and
    # target mapped to their counts.
    
    def generate_voc(self):
        tokenized_q = nltk.word_tokenize(self.question.q)
        tokenized_target = nltk.word_tokenize(self.question.target)
        query_terms = tokenized_q + tokenized_target

        # TODO: Decide how to handle punctuation within tokens. For now, just delete it.
        # Consider replacing hyphens with spaces (would want to do this before tokenizing).

#       sys.stderr.write("DEBUG  Here are the query terms before stripping interior punctuation: %s\n" % query_terms)
        for i in range(len(query_terms)):
        	query_terms[i] = re.sub(r'\W', '', query_terms[i])
        query_terms = filter(lambda x: x != '', query_terms)
       
#       sys.stderr.write("DEBUG  Here are the query terms after punctuation stripping: %s\n" % query_terms)
        query_dict = {}

        for term in query_terms:
            if query_dict.get(term) == None:
                query_dict[term] = 1
            else:
                query_dict[term] += 1
        
#       sys.stderr.write("DEBUG  Here is the query vocabulary: %s\n" % query_dict)
        return query_dict


	# This method returns a list of SearchQuery objects.
	
    def generate_queries(self):
        # NB: For now, the weights of the search terms in the SearchQuery are equal to the
        # counts of the term in the question plus the target.
        query = SearchQuery(self.query_voc, 1)
#       sys.stderr.write("DEBUG  Here is the search query: %s\n" % query.to_string())

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
            ans_template = AnswerTemplate(set(self.query_voc.keys()))
#           sys.stderr.write("DEBUG  Here is the answer template: %s\n" % ans_template.to_string())
            
            return ans_template

        else:
            sys.stderr.write("Warning: System can only handle \"factoid\" questions\n")
