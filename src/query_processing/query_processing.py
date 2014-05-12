# LING 573 Question Answering System
# Code last updated 4/22/14 by Andrea Kahn
#
# This code implements a QueryProcessor for the question answering system.


import sys
import nltk
import re
from general_classes import *
from collections import defaultdict


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
#       sys.stderr.write("DEBUG  Here is the search query: %s\n" % query)
        return [query]


	# This method returns an AnswerTemplate object.
	
    def generate_ans_template(self):
	
		# NB: The following if statement should always evaluate as True in our system, but
		# its inclusion enables the system to more easily be extended to handle other types
		# of questions, for which the text-processing and AnswerTemplate-generation steps
		# might be slightlydifferent.

        if self.question.type=="FACTOID":
            # by default, assign all answer types some small weight
            ans_types = defaultdict(lambda: 0.1)
            sys.stderr.write("\nDEBUG  Here is the question: %s\n" % self.question.q)
            
            # attempt to predict certain answer type using rules and set relevant weights accordingly
            person_match = re.compile(r'\b[Ww]+ho\b|\b[Ww]+hat (?:is|was) (?:his|her) name\b').search(self.question.q)
            name_match = re.compile(r'\b[Ww]+hat (?:is|was) (?:the|its|their) name\b').search(self.question.q)
            loc_match = re.compile(r'\b[Ww]here\b|\b(?:[Ww]hat|[Ww]hich) (?:(?:is|was) the )?(?:city|state|province|territory|country|continent)\b').search(self.question.q)
            time_match = re.compile(r'\b[Ww]hen\b|\b(?:[Ww]hat|[Ww]hich) (?:(?:is|was) the )?(?:date|day|month|year|decade|century)\b').search(self.question.q)
            num_match = re.compile(r'\b[Hh]ow (?:much|many)\b').search(self.question.q)
            
#           for query_term in self.query_voc.keys():
#           if query_term.lower() in ['who']:
            if person_match:
                sys.stderr.write("DEBUG  Query contains %s; setting person weight\n" % person_match)
                ans_types['person'] = 0.9
            if name_match:
                sys.stderr.write("DEBUG  Query contains %s; setting person and organization weight\n" % name_match)
                ans_types['person'] = 0.9
                ans_types['organization'] = 0.9
                ans_type['object'] = 0.9
#           if query_term.lower() in ['where']:
            if loc_match:
                sys.stderr.write("DEBUG  Query contains %s; setting location weight\n" % loc_match)
                ans_types['location'] = 0.9
#           if query_term.lower() in ['when']:
            if time_match:
                sys.stderr.write("DEBUG  Query contains %s; setting time_ex weight\n" % time_match)
                ans_types['time_ex'] = 0.9
            if num_match:
                sys.stderr.write("DEBUG  Query contains %s; setting number weight\n" % num_match)
                ans_types['number'] = 0.9                

            # generate a corresponding AnswerTemplate object
            ans_template = AnswerTemplate(self.question.id,set(self.query_voc.keys()),ans_types)
            sys.stderr.write("DEBUG  Here is the answer template: %s\n" % ans_template.type_weights)
            
            return ans_template

        else:
            sys.stderr.write("Warning: System can only handle \"factoid\" questions\n")
