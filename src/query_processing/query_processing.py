# LING 573 Question Answering System
# Code last updated 5/19/14 by Andrea Kahn
#
# This code implements a QueryProcessor for the question answering system.


import sys
import nltk
import re
from general_classes import *
from collections import defaultdict
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
semcor_ic = wordnet_ic.ic('ic-semcor.dat')
from nltk.corpus import lin_thesaurus as thes
import heapq


# A QueryProcessor object has the attribute "question", a Question object.

class QueryProcessor(object):

    def __init__(self, question, stoplist=None):
        self.question = question
        self.stoplist = stoplist
        self.query_voc = self.generate_voc()



    # This method returns a dictionary of unigrams appearing in the original question and
    # target mapped to their counts.
    
    def generate_voc(self):
        tokenized_q = nltk.word_tokenize(self.question.q)

        # NEs are removed from query_terms and added to self.ne
        # Note: had to strip punctuation from self.ne too, to avoid Indri freakout
        tokenized_q, self.ne = self.extract_ne(tokenized_q)

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
            if term.lower() not in self.stoplist:
                if query_dict.get(term) == None:
                    query_dict[term] = 1
                else:
                    query_dict[term] += 1
#           else:
#               sys.stderr.write("DEBUG  Removing stopword %s from query\n" % term)

#       sys.stderr.write("DEBUG  Here is the query vocabulary: %s\n" % query_dict)
        return query_dict



	# This method returns a list of SearchQuery objects.
	
    def generate_queries(self):
        # For now, the weights of the search terms in the SearchQuery are equal to the
        # counts of the term in the question plus the target.
        # For now, just assign this query weight 1 (we can experiment with different weighting
        # schemes).

        queries = []

        initial_query = SearchQuery(self.query_voc, 1)
#       sys.stderr.write("DEBUG  Here is the initial query: %s\n" % initial_query)
        queries.append(initial_query)
        
        #expanded_query = self.expand_query()
        #queries.append(expanded_query)

        # put NEs back into both expanded and initial query objects
        # TODO: note - do we want to upweight the NEs?

        for term in self.ne:
            for query in queries:
                if query.search_terms.get(term) == None:
                    query.search_terms[term] = 1
                else:
                    query.search_terms[term] += 1

#       sys.stderr.write("DEBUG  Here are the queries generated: %s\n" % [str(initial_query), str(expanded_query)])
        return queries



    # This method uses NLTK's Lin thesaurus corpus to expand the initial query to form a second query containing
    # the initial query terms and their top n synonyms (for now, n=3; we can experiment
    # with different n to figure out what's optimal--and maybe we want a different
    # n for different POSs), then returns the expanded query.
    #
    # TODO: Consider POS-tagging the query terms first and passing the expected POS (perhaps
    # just categorized as noun, verb, or adj, ignoring queries that do not fall into
    # these categories) to the expand_query method, which will filter synonyms accordingly.
    #
    # For now, since we still have a lot of work to do to prevent query expansion from
    # introducing crazy errors, just assign this query weight 0 (we can experiment with
    # different weighting schemes).

    def expand_query(self):

        expanded_voc = {}
        for term in self.query_voc:
            # copy the term and its weight to the dictionary for the expanded query
            expanded_voc[term] = self.query_voc[term]
            # get the top 3 synonyms of the term and their similarity measures
            term_syns = self.expand_term(term, 3)
            for item in term_syns:
                # unpack the 2-tuple of synonym and similarity measure
                syn, sim_measure = item
                # add the synonym to the dictionary for the expanded query, assigning it
                # weight = weight of original term * similarity measure of synonym
                expanded_voc[syn] = expanded_voc[term] * sim_measure
        expanded_query = SearchQuery(expanded_voc, 0)
        return expanded_query


    
    # This method takes a query term (string) and a maximum number of synonyms to return (int)
    # as arguments and returns a list of 2-tuples in which the first element is the synonym
    # and the second element is the similarity to the query term.
    # TODO: Incorporate POS tagging of the question (perhaps in the generate_queries method),
    # then have the below method take a POS as a second element, then filter so we only
    # expand the query with terms that are the correct POS. POS appear to be simA.lsp,
    # simV.lsp, and simN.lsp. Maybe we just want to expand query terms whose POS tags fall
    # under the categories of adj, verb, and noun (this would have the added bonus of removing
    # a lot of stopwords automatically).
    
    def expand_term(self, term, num_syns):
#       sys.stderr.write("DEBUG  Getting scored synonyms of %s\n" % term)
        syns = thes.scored_synonyms(term)
#       sys.stderr.write("DEBUG  Here are the synsets returned from the Lin thesaurus: %s\n" % syns)

        all_syns = []
        # syn list is in the form ((POS, [syn, syn, syn]), (POS, [syn, syn, syn]) ...)
        # concatenate all synonyms from the various lists (see TODO for possible change)
        for element in syns:
            all_syns.extend(element[1])
#       sys.stderr.write("DEBUG  Here are all the synonyms: %s\n" % all_syns)
        
        if len(all_syns) > num_syns:
#           sys.stderr.write("DEBUG  Found more synonyms than required; filtering by similarity measure\n")
            # get n-best synonyms according to Lin similarity
            top = heapq.nlargest(num_syns, all_syns, key = lambda k: k[1])
        else:
#           sys.stderr.write("DEBUG  Synonyms found do not exceed max number of synonyms desired; skipping filtering step\n")
            top = all_syns
#       sys.stderr.write("DEBUG  Here are the top %s synonyms: %s\n" % (num_syns, top))
        return top



	# This method performs question classification using regular expressions, then generates
	# and returns an AnswerTemplate object.
	
    def generate_ans_template(self):
	
		# NB: The following if statement should always evaluate as True in our system, but
		# its inclusion enables the system to more easily be extended to handle other types
		# of questions, for which the text-processing and AnswerTemplate-generation steps
		# might be slightlydifferent.

        if self.question.type=="FACTOID":
            # by default, assign all answer types some small weight
            ans_types = defaultdict(lambda: 0.1)
#           sys.stderr.write("\nDEBUG  Here is the question: %s\n" % self.question.q)
         
            # attempt to predict certain answer type using rules and set relevant weights accordingly
            person_match = re.compile(r'\b[Ww]+ho\b|\b[Ww]+hat (?:is|was) (?:his|her) name\b').search(self.question.q)
            name_match = re.compile(r'\b[Ww]+hat (?:is|was) (?:the|its|their) name\b').search(self.question.q)
            loc_match = re.compile(r'\b[Ww]here\b|\b(?:[Ww]hat|[Ww]hich) (?:(?:is|was) the )?(?:city|state|province|territory|country|continent)\b').search(self.question.q)
            time_match = re.compile(r'\b[Ww]hen\b|\b(?:[Ww]hat|[Ww]hich) (?:(?:is|was) the )?(?:date|day|month|year|decade|century)\b').search(self.question.q)
            num_match = re.compile(r'\b[Hh]ow (?:much|many)\b').search(self.question.q)

            match_found = False

            if person_match:
#               sys.stderr.write("DEBUG  Query contains %s; setting person weight\n" % person_match.group(0))
                ans_types['person'] = 0.9
                match_found = True
            if name_match:
#               sys.stderr.write("DEBUG  Query contains %s; setting person and organization weight\n" % name_match.group(0))
                ans_types['person'] = 0.9
                ans_types['organization'] = 0.9
                ans_types['object'] = 0.9
                match_found = True
            if loc_match:
#               sys.stderr.write("DEBUG  Query contains %s; setting location weight\n" % loc_match.group(0))
                ans_types['location'] = 0.9
                match_found = True
            if time_match:
#               sys.stderr.write("DEBUG  Query contains %s; setting time_ex weight\n" % time_match.group(0))
                ans_types['time_ex'] = 0.9
                match_found = True
            if num_match:
#               sys.stderr.write("DEBUG  Query contains %s; setting number weight\n" % num_match.group(0))
                ans_types['number'] = 0.9
                match_found = True
                
            if not match_found:
                ans_types['other'] = 0.5               

            # generate a corresponding AnswerTemplate object
            ans_template = AnswerTemplate(self.question.id,set(self.query_voc.keys()),ans_types)
#           sys.stderr.write("DEBUG  Here is the answer template: %s\n" % ans_template.type_weights)
            
            return ans_template

        else:
            sys.stderr.write("Warning: System can only handle \"factoid\" questions\n")



    # This method takes a list of query tokens (strings) as input and returns a 2-tuple in
    # which the first element is a list of the query tokens that are not named entities and
    # the second element is a list of the named entities (strings).

    def extract_ne(self, tokenized_q):

        ne = []
        non_ne = tokenized_q

        pos_tags = nltk.pos_tag(tokenized_q)
        extracted = nltk.ne_chunk(pos_tags, binary=True)
        # find NE-headed subtrees
        for subtree in extracted.subtrees(lambda t: t.node == "NE"):
            leaves = subtree.leaves()
            # add space-delimited NE phrases to ne list
            current_ne = ' '.join(leaf[0] for leaf in leaves)
            ne.append(current_ne)
            # note: this isn't foolproof, but should work for now. I can't figure out how to get
            # the indices of the NE terms in the surface string
            for leaf in leaves:
                #sys.stderr.write("trying to remove "+leaf[0]+" from "+str(non_ne)+"\n")
                non_ne.remove(leaf[0])

        return non_ne, ne
