# LING 573 Question Answering System
# Code last updated 4/15/14 by Andrea Kahn
# This code holds classes that need to be accessed by various parts of the system.


# A Question object has the attributes id (a float corresponding to the TREC question ID),
# type (a string corresponding to the question type; always "factoid" in our system, but
# could take on other values in an extended version of the system), q (a string corresponding
# to the TREC natural-language question), and target (a string corresponding to the context
# given for a set of questions in TREC 2004 and 2005; defaults to None).

# The wrapper file generates Question objects from a TREC document and passes each one into
# the question-answering pipeline, beginning with the query-processing module.

class Question(object):
	def __init__(self, id, type, q, target=None):
		self.id = id
		self.type = type
		self.q = q
		self.target = target
	
	# This method returns a string representing the Question instance (used for debugging).
	def to_string(self):
		to_return = "id: %s; type: %s; q: %s; target: %s" % (self.id, self.type, self.q, self.target)
		return to_return	


# A SearchQuery object has the attributes search_terms (a set of strings, each of which can
# be one or more words) and weight (which will be used to calculate the probability of the
# corresponding AnswerCandidate, with a higher weight corresponding to a higher probability).

# The query_processing module outputs a set of SearchQuery objects that are passed to the
# info_retrieval module as input. 

class SearchQuery(object):
	def __init__(self, search_terms, weight):
		self.search_terms = search_terms
		self.weight = weight
	
	# This method returns a string representing the SearchQuery instance (used for debugging).
	def to_string(self):
		to_return = "search_terms: %s; weight: %s" % (self.search_terms, self.weight)
		return to_return


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

