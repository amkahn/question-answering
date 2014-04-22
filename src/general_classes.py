# LING 573 Question Answering System
# Code last updated 4/22/14 by Andrea Kahn
#
# This code holds classes that need to be accessed by various parts of the system.


from collections import defaultdict


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


# A SearchQuery object has the attributes search_terms (a dictionary of strings, each of
# which can be one or more words, mapped to weights for those terms) and weight (which will
# be used to calculate the probability of the corresponding AnswerCandidate, with a higher
# weight corresponding to a higher probability of that answer being correct).

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


# An AnswerTemplate object has the attributes query_terms (a set of basic search query terms
# from the original question) and type_weights (a dictionary for the weights of each NE type,
# where the weights will be used to reweight AnswerCandidate objects).

class AnswerTemplate:
    def __init__(self,query_terms):
        # should the AnswerTemplate get the question and then generate the template from that?
        # or should the QueryProcessor generate the pieces and then pass them to the AnswerTemplate
        self.query_terms = query_terms
        # should the default weight of a type be 0 or some small number?
        self.type_weights = defaultdict(lambda:0)
        # by default, set weights for person, organization, and location to 1
        for x in ["person","organization","location"]:
            self.type_weights[x] = 1

    # This method returns a string representing the AnswerTemplate instance (used for debugging).
    def to_string(self):
        to_return = "query_terms: %s; type_weights: %s" % (self.query_terms, self.type_weights)
        return to_return

    # This method changes the weight of the given type to the given weight.
    # If the type is not already in the type_weights dictionary, it is added.
    def set_weight(type,weight):
        self.type_weights[type] = weight

    # one possibility - AnswerTemplate generates the template
    def generate_template(self):
        # do something here to figure out NE type
        # or alternatively, gather probabilities for all different NE types
        pass


# A Passage object has the attributes passage (a string), weight (a float), and doc_id (a
# float). This is a wrapper class for passages and weights returned by indri/lemur. 

class Passage:
    def __init__(self, passage, weight, doc_id):
        self.passage = passage
        self.weight = weight
        # I'm adding something here for the ID of the doc the passage came from
        # feel free to modify, just using for testing the AnswerProcessor - Claire
        self.doc_id = doc_id

