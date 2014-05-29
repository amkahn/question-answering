# LING 573 Question Answering System
# Code last updated 5/23/14 by Andrea Kahn
#
# This code implements a QueryProcessor for the question answering system.


import sys
import nltk
import re
from general_classes import *
from collections import defaultdict
from nltk.corpus import lin_thesaurus as thes
import heapq
from copy import deepcopy


# A QueryProcessor object has the attribute "question", a Question object; "stoplist", a
# list of stopwords (strings); "web_snippets", a list of web snippets (strings);
# "non_ne_voc", a list of non-named entities appearing in the question and target mapped
# to counts; "ne_voc", a list of named-entity terms appearing in the question and target
# mapped to counts; and query_voc, a list of all query terms (including named entities).

class QueryProcessor(object):

    def __init__(self, question, stoplist=None, web_snippets=None):
        self.question = question
        self.stoplist = stoplist
        self.web_snippets = web_snippets
        self.non_ne_voc, self.ne_voc, self.query_voc = self.generate_voc()


    # This method returns a dictionary of unigrams appearing in the original question and
    # target mapped to their counts.
    
    def generate_voc(self):
        tokenized_q = nltk.word_tokenize(self.question.q)
        tokenized_target = nltk.word_tokenize(self.question.target)

        # separate named entities from non-named entities in question and target, respectively
        # Note: had to strip punctuation from named entities, to avoid Indri freakout -Clara
        # I'm not sure if punctuation-stripping on NEs is actually happening -Andrea
        q_non_ne, q_ne = self.extract_ne(tokenized_q)
        
        # The following three lines of code, which perform NE extraction on the target and
        # add the named-entity and non-named entity output to the appropriate lists of
        # question/target terms, caused our accuracy to drop significantly.
#       target_non_ne, target_ne = self.extract_ne(tokenized_target)
#       non_ne = q_non_ne + target_non_ne
#       ne = q_ne + target_ne

        # Instead, add the tokenized target to the list of non-named entity terms.
#       non_ne = q_non_ne + tokenized_target
#       ne = q_ne

        # Or, for slightly better results, add the tokenized target to the list of named-entity
        # terms. (Currently, the only difference between this and the previous code block
        # is that stopwords don't get filtered from the target -- filtering them causes an
        # increase in our strict score but a drop in our lenient score.)
        non_ne = q_non_ne
        ne = q_ne + tokenized_target
            
#       sys.stderr.write("DEBUG QUERY_PROCESSING.GENERATE_VOC()  Here are the non-named entities in the question and target: %s\n" % non_ne)
#       sys.stderr.write("DEBUG QUERY_PROCESSING.GENERATE_VOC()  Here are the named entities in the question and target: %s\n" % ne)
        
        # Code for deleting punctuation (no longer used as we do base64 encoding in IR and
        # doing punctuation-stripping here hurts our accuracy).
#       sys.stderr.write("DEBUG  Here are the non-named entity query terms before punctuation stripping: %s\n" % non_ne)
#       for i in range(len(non_ne)):
#           non_ne[i] = re.sub(r'\W', '', non_ne[i])
#       non_ne = filter(lambda x: x != '', non_ne)

#       sys.stderr.write("DEBUG  Here are the non-named entity query terms after punctuation stripping: %s\n" % non_ne)
        non_ne_dict = {}

        # Create a dictionary of all non-named entity terms, excluding stopwords, mapped to counts in the question/target
        for term in non_ne:
            term = term.lower()
            if term not in self.stoplist:
                if non_ne_dict.get(term) == None:
                    non_ne_dict[term] = 1
                else:
                    non_ne_dict[term] += 1
#           else:
#               sys.stderr.write("DEBUG  Removing stopword %s from query\n" % term)
        
        ne_dict = {}
        
        # Create a dictionary of all named entities mapped to counts in the question/target
        for term in ne:
            term = term.lower()
            if ne_dict.get(term) == None:
                ne_dict[term] = 1
            else:
                ne_dict[term] += 1
        
        # Create a dictionary of all terms (named entities and non-named entities) mapped to counts in the question/target
        query_dict = deepcopy(non_ne_dict)
        
        for ne, count in ne_dict.items():
            if query_dict.get(ne) == None:
                query_dict[ne] = count
            else:
                query_dict[ne] += count
                    
#       sys.stderr.write("DEBUG QUERY_PROCESSING.GENERATE_VOC()  Here is the frequency dictionary of all terms in the question and target: %s\n" % query_dict)

        return non_ne_dict, ne_dict, query_dict



    # This method returns a list of SearchQuery objects.
    
    def generate_queries(self):
        # For now, the weights of the search terms in the SearchQuery are equal to the
        # counts of the term in the question plus the target.
        # For now, just assign this query weight 1 (we can experiment with different weighting
        # schemes).

        queries = []

        initial_query = SearchQuery(self.query_voc, 1)
        #sys.stderr.write("DEBUG  Here is the initial query for question %s: %s\n" % (self.question.id, initial_query))
#       queries.append(initial_query)
        
        # Create another query using web redundancy expansion with the top 5 unigrams, weights
        # of 0.5 for the query terms, and a weight of 1 for the query.
        web_expanded_query = self.web_expand_query(5, 0.5, 1)
        #sys.stderr.write("DEBUG  Here is the web redundancy-expanded query for question %s: %s\n" % (self.question.id, web_expanded_query))
        queries.append(web_expanded_query)
        
        #lin_expanded_query = self.lin_expand_query()
        #queries.append(lin_expanded_query)

        # TODO: put NEs back into expanded query objects
        # TODO: note - do we want to upweight the NEs? (here and elsewhere)

#         for term in self.ne:
#             for query in queries:
#                 if query.search_terms.get(term) == None:
#                     query.search_terms[term] = 1
#                 else:
#                     query.search_terms[term] += 1

#       sys.stderr.write("DEBUG  Here are the queries generated: %s\n" % queries)
        return queries



    # This method uses NLTK's Lin thesaurus corpus to expand the initial query to form a
    # second query containing the initial query terms and their top n synonyms (for now,
    # n=3; we can experiment with different n to figure out what's optimal--and maybe we
    # want a different n for different POSs), then returns the expanded query.
    #
    # TODO: Consider POS-tagging the query terms first and passing the expected POS (perhaps
    # just categorized as noun, verb, or adj, ignoring queries that do not fall into
    # these categories) to the lin_expand_query method, which will filter synonyms accordingly.
    #
    # For now, since we still have a lot of work to do to prevent query expansion from
    # introducing crazy errors, just assign this query weight 0 (we can experiment with
    # different weighting schemes).

    def lin_expand_query(self):

        expanded_voc = {}
        for term in self.query_voc:
            # copy the term and its weight to the dictionary for the expanded query
            expanded_voc[term] = self.non_ne_voc[term]
            # get the top 3 synonyms of the term and their similarity measures
            term_syns = self.get_lin_terms(term, 3)
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
    
    def get_lin_terms(self, term, num_syns):
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



    # This method takes as input the number of top unigrams to return (an int), a weight
    # for the unigrams, and a weight for the expanded query; generates a SearchQuery object
    # incorporating both the initial query vocabulary and the top n query terms; and then
    # returns the expanded query.
    
    def web_expand_query(self, num_unigrams, unigram_weight, query_weight):
        expanded_voc = deepcopy(self.query_voc)
        top_web_unigrams = self.get_web_unigrams(num_unigrams)
        for unigram in top_web_unigrams:
            expanded_voc[unigram] = unigram_weight
        expanded_query = SearchQuery(expanded_voc, query_weight)
        return expanded_query
    
    
    
    # This method takes as input the number of top unigrams to return (an int) and returns
    # a list of most frequent unigrams (strings) appearing in the web snippets.
    
    def get_web_unigrams(self, n):
        unigrams = defaultdict(int)
        
        for snippet in self.web_snippets:
            # Tokenize the snippets
            # TODO: UTF-8 encoding
            sentences = []
            snippet_chunks = snippet.lower().split('...')
            for chunk in snippet_chunks:
                sentences.extend(nltk.sent_tokenize(chunk))
#           sys.stderr.write("DEBUG  Here is the list of sentences from the web snippet: %s\n" % sentences)
            tokens = []
            for sentence in sentences:
                tokens.extend(nltk.word_tokenize(sentence))
            #sys.stderr.write("DEBUG  Here is the list of tokens from the web snippet: %s\n" % tokens)

            # Strip punctuation from tokens, which are strings but I'm not sure of the encoding
            # TODO: how to deal with hyphens?
            for i in range(len(tokens)):
                tokens[i] = re.sub(r'\W', '', tokens[i])
            tokens = filter(lambda x: x != '', tokens)
            
            # Add the unigrams to frequency dictionary if they are not stopwords and not
            # terms in the initial query
            for i in range(len(tokens)):
                if not tokens[i] in self.stoplist and not tokens[i] in self.query_voc.keys():
                    unigrams[tokens[i]] += 1

        return heapq.nlargest(n, unigrams, key=lambda k: unigrams[k])



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
#           sys.stderr.write("DEBUG  Here is the answer template: %s\n" % ans_template)
            
            return ans_template

        else:
            sys.stderr.write("Warning: System can only handle \"factoid\" questions\n")



    # This method takes a list of tokens (strings) as input and returns a 2-tuple in which
    # the first element is a list of the tokens that are not named entities (strings) and
    # the second element is a list of the named entities (strings).

    def extract_ne(self, input):
#       sys.stderr.write("DEBUG QUERY_PROCESSING.EXTRACT_NE()  Here is the input: %s\n" % input)
        
        ne = []
        non_ne = input

        pos_tags = nltk.pos_tag(input)
        extracted = nltk.ne_chunk(pos_tags, binary=True)
        # find NE-headed subtrees
        for subtree in extracted.subtrees(lambda t: t.node == "NE"):
            leaves = subtree.leaves()
            # add space-delimited NE phrases to ne list
            current_ne = ' '.join(leaf[0] for leaf in leaves)
            ne.append(current_ne)
            # note: this isn't foolproof, but should work for now. I can't figure out how to get
            # the indices of the NE terms in the surface string -Clara
            for leaf in leaves:
                #sys.stderr.write("trying to remove "+leaf[0]+" from "+str(non_ne)+"\n")
                non_ne.remove(leaf[0])
        
#       sys.stderr.write("DEBUG QUERY_PROCESSING.EXTRACT_NE()  Here is the list of non-named entities: %s\n" % non_ne)
#       sys.stderr.write("DEBUG QUERY_PROCESSING.EXTRACT_NE()  Here is the list of named entities: %s\n" % ne)

        return non_ne, ne      
