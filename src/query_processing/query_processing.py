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


# A QueryProcessor object has the attributes "parameters", the parameters dictionary
# generated by the wrapper script; "question", a Question object; "stoplist", a list of
# stopwords (strings); "web_snippets", a list of web snippets (strings); "non_ne_pos_tagged",
# a list of tuples in which the first element is a non-named entity appearing in the question
# and the second element is its POS tag; "non_ne_voc", a list of non-named entities appearing
# in the question mapped to counts (i.e., terms eligible for query expansion); and "query_voc",
# a list of all query terms (including named entities) in the question and target.

class QueryProcessor(object):

    def __init__(self, parameters, question, stoplist, web_snippets):
        self.parameters = parameters
        self.question = question
        self.stoplist = stoplist
        self.web_snippets = web_snippets
        self.non_ne_voc, self.query_voc, self.non_ne_pos_tagged = self.generate_voc()

    # This method returns a dictionary of unigrams appearing in the original question and
    # target mapped to their counts.
    
    def generate_voc(self):
        tokenized_q = nltk.word_tokenize(self.question.q)
        tokenized_target = nltk.word_tokenize(self.question.target)

        # Separate named entities from non-named entities in question.
        # Note: had to strip punctuation from named entities, to avoid Indri freakout -Clara
        # I'm not sure if punctuation-stripping on NEs is actually happening -Andrea
        q_non_ne, q_ne, q_non_ne_pos_tagged = self.extract_ne(tokenized_q)
        
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
#       non_ne = q_non_ne
#       ne = q_ne + tokenized_target
            
#       sys.stderr.write("DEBUG QUERY_PROCESSING.GENERATE_VOC()  Here are the non-named entities in the question and target: %s\n" % non_ne)
#       sys.stderr.write("DEBUG QUERY_PROCESSING.GENERATE_VOC()  Here are the named entities in the question and target: %s\n" % ne)
        
        # Code for deleting punctuation (no longer used as we do base64 encoding in IR and
        # doing punctuation-stripping here hurts our accuracy).
#       sys.stderr.write("DEBUG  Here are the non-named entity query terms before punctuation stripping: %s\n" % non_ne)
#       for i in range(len(non_ne)):
#           non_ne[i] = re.sub(r'\W', '', non_ne[i])
#       non_ne = filter(lambda x: x != '', non_ne)
#       sys.stderr.write("DEBUG  Here are the non-named entity query terms after punctuation stripping: %s\n" % non_ne)

        # trying out method where only standalone punctuation is removed
        for i in range(len(q_non_ne)):
            q_non_ne[i] = re.sub(r'^\W$','',q_non_ne[i])
        q_non_ne = filter(lambda x: x != '',q_non_ne)


        # Create a dictionary of all non-named entity terms, excluding stopwords, mapped
        # to counts in the question/target.
        non_ne_dict = {}
        for term in q_non_ne:
            term = term.lower()
            if term not in self.stoplist:
                if non_ne_dict.get(term) == None:
                    non_ne_dict[term] = 1
                else:
                    non_ne_dict[term] += 1
#           else:
#               sys.stderr.write("DEBUG  Removing stopword %s from query\n" % term)
        
        
        # Create a dictionary of all terms (non-named entities, named entities, and target
        # tokens) mapped to counts in the question/target.
        
        # Start with existing dictionary of non-named entities.
        query_dict = deepcopy(non_ne_dict)
        
        # Add the named entities.
        for term in q_ne:
            term = term.lower()
            if query_dict.get(term) == None:
                query_dict[term] = (1 * float(self.parameters['ne_upweighting']))
            else:
                query_dict[term] += (1 * float(self.parameters['ne_upweighting']))

        # Add the target tokens.
        if self.parameters['stopword_filter_target']:
            tokenized_target = filter(lambda x: x not in self.stoplist, tokenized_target)
        
        for term in tokenized_target:
            term = term.lower()
            
            if query_dict.get(term) == None:
                query_dict[term] = (1 * float(self.parameters['target_upweighting']))
            else:
                query_dict[term] += (1 * float(self.parameters['target_upweighting']))
                  
#       sys.stderr.write("DEBUG QUERY_PROCESSING.GENERATE_VOC()  Here is the frequency dictionary of all terms in the question and target: %s\n" % query_dict)

        return non_ne_dict, query_dict, q_non_ne_pos_tagged



    # This method returns a list of SearchQuery objects.
    
    def generate_queries(self):
        queries = []
        
        # Create an initial query in which the weights of the search terms are equal to the
        # counts of the term in the question plus the target.
        # For now, just assign this query weight 1 (we can experiment with different weighting
        # schemes).
        initial_query = SearchQuery(self.query_voc, 1)
#       sys.stderr.write("DEBUG  Here is the initial query for question %s: %s\n" % (self.question.id, initial_query))
#       queries.append(initial_query)
        
        # Create another query using web redundancy expansion. For now, set weight to 1.
        web_expanded_query = self.web_expand_query(initial_query, int(self.parameters['num_web_exp_terms']), float(self.parameters['weight_web_exp_terms']), 1)
        #sys.stderr.write("DEBUG  Here is the web redundancy-expanded query for question %s: %s\n" % (self.question.id, web_expanded_query))
        queries.append(web_expanded_query)
        
        lin_expanded_query = self.lin_expand_query(initial_query, int(self.parameters['num_lin_exp_terms']), float(self.parameters['weight_lin_exp_query']))
        queries.append(lin_expanded_query)

#       sys.stderr.write("DEBUG  Here are the queries generated: %s\n" % queries)
        return queries



    # This method uses NLTK's Lin thesaurus corpus to expand the initial query to form a
    # second query containing the initial query terms and their top n synonyms (for now,
    # n=3; we can experiment with different n to figure out what's optimal--and maybe we
    # want a different n for different POSs), and the returns a new query that is an
    # expanded version of the input query.
    #
    # TODO: Consider POS-tagging the query terms first and passing the expected POS (perhaps
    # just categorized as noun, verb, or adj, ignoring queries that do not fall into
    # these categories) to the lin_expand_query method, which will filter synonyms accordingly.

    def lin_expand_query(self, query_to_expand, num_syns, query_weight):
        # Copy the query-term dictionary from the query to expand.
        expanded_voc = deepcopy(query_to_expand.search_terms)

        # Remove duplicates. (Note that this will only remove a duplicate token if both
        # occurrences have the same POS).
        to_expand = set(self.non_ne_pos_tagged)
#       sys.stderr.write("DEBUG  Here is the set of terms to Lin-expand: %s\n" % to_expand)
        
        # Filter out stopwords.
        to_expand = filter(lambda x: x[0] not in self.stoplist, to_expand)
#       sys.stderr.write("DEBUG  Here is the set of terms to Lin-expand after stopword filtering: %s\n" % to_expand)
        
        # For each non-named entity (note that if a term appears twice in the question,
        # we'll do this twice):
        for pair in to_expand:
            # Get the top n synonyms of the term and their similarity measures for nouns and verbs.
            if pair[1] in ['NN', 'NNS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
                if pair[1] in ['NN', 'NNS']:
                    term_syns = self.get_lin_terms(pair[0], num_syns, 'simN.lsp')
                else:
                    term_syns = self.get_lin_terms(pair[0], num_syns, 'simV.lsp')
                for item in term_syns:
                    # Unpack the 2-tuple of synonym and similarity measure.
                    syn, sim_measure = item
                    # Add the synonym to the dictionary for the expanded query, assigning it
                    # weight = weight of original term * similarity measure of synonym.
                    if expanded_voc.get(syn) != None:
                        expanded_voc[syn] = self.non_ne_voc[pair[0]] * sim_measure
        expanded_query = SearchQuery(expanded_voc, query_weight)
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
    
    def get_lin_terms(self, term, n, pos):
#       sys.stderr.write("DEBUG  Getting scored synonyms of term %s, POS %s\n" % (term, pos))
        syns = thes.scored_synonyms(term)
#       sys.stderr.write("DEBUG  Here are the synsets returned from the Lin thesaurus: %s\n" % syns)

        all_syns = []
        # syn list is in the form ((POS, [syn, syn, syn]), (POS, [syn, syn, syn]) ...)
        # concatenate all synonyms from the various lists (see TODO for possible change)
        for element in syns:
            if element[0] == pos:
                all_syns.extend(element[1])
#       sys.stderr.write("DEBUG  Here are all the synonyms: %s\n" % all_syns)
        
        if len(all_syns) > n:
#           sys.stderr.write("DEBUG  Found more synonyms than required; filtering by similarity measure\n")
            # get n-best synonyms according to Lin similarity
            top = heapq.nlargest(n, all_syns, key = lambda k: k[1])
        else:
#           sys.stderr.write("DEBUG  Synonyms found do not exceed max number of synonyms desired; skipping filtering step\n")
            top = all_syns
#       sys.stderr.write("DEBUG  Here are the top %s synonyms: %s\n" % (n, top))
        return top



    # This method takes as input a SearchQuery object to expand, the number of top unigrams
    # to return (an int), a weight for the unigrams, and a weight for the expanded query;
    # generates a NEW SearchQuery object incorporating both the initial query vocabulary
    # and the top n web unigrams; and then returns the new SearchQuery object.
    
    def web_expand_query(self, query_to_expand, num_unigrams, unigram_weight, query_weight):
        # Copy the query-term dictionary from the query to expand.
        expanded_voc = deepcopy(query_to_expand.search_terms)
        top_web_unigrams = self.get_web_unigrams(num_unigrams, query_to_expand.search_terms)
        for unigram in top_web_unigrams:
            expanded_voc[unigram] = unigram_weight
        expanded_query = SearchQuery(expanded_voc, query_weight)
        return expanded_query
    
    
    
    # This method takes as input the number of top unigrams to return (an int) and a list
    # of terms to be excluded (namely, terms already in the query that is being expanded),
    # and returns a list of most frequent unigrams appearing in the web snippets.
    
    def get_web_unigrams(self, n, terms_to_exclude):
        unigrams = defaultdict(int)
        
        for snippet in self.web_snippets:
            # Tokenize the snippets.
            sentences = []
            snippet_chunks = snippet.lower().split('...')
            for chunk in snippet_chunks:
                sentences.extend(nltk.sent_tokenize(chunk))
#           sys.stderr.write("DEBUG  Here is the list of sentences from the web snippet: %s\n" % sentences)
            tokens = []
            for sentence in sentences:
                tokens.extend(nltk.word_tokenize(sentence))
            #sys.stderr.write("DEBUG  Here is the list of tokens from the web snippet: %s\n" % tokens)

            # Strip punctuation from tokens.
            for i in range(len(tokens)):
                tokens[i] = re.sub(r'\W', '', tokens[i])
            tokens = filter(lambda x: x != '', tokens)
            
            # Add the unigrams to frequency dictionary if they are not stopwords and not
            # terms in the initial query.
            for i in range(len(tokens)):
                if not tokens[i] in self.stoplist and not tokens[i] in terms_to_exclude:
                    unigrams[tokens[i]] += 1

        # Return n most frequent unigrams.
        return heapq.nlargest(n, unigrams, key=lambda k: unigrams[k])



    # This method performs question classification using regular expressions, then generates
    # and returns an AnswerTemplate object.
    
    def generate_ans_template(self):
    
        # NB: The following if statement should always evaluate as True in our system, but
        # its inclusion enables the system to more easily be extended to handle other types
        # of questions, for which the text-processing and AnswerTemplate-generation steps
        # might be slightlydifferent.

        if self.question.type=="FACTOID":

            # By default, assign all answer types some small weight.
            ans_types = defaultdict(lambda: 0.1)
#           sys.stderr.write("\nDEBUG  Here is the question: %s\n" % self.question.q)
         
            # Attempt to predict certain answer type using rules and set relevant weights accordingly.
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

            # Generate a corresponding AnswerTemplate object.
            ans_template = AnswerTemplate(self.question.id,set(self.query_voc.keys()),ans_types)
#           sys.stderr.write("DEBUG  Here is the answer template: %s\n" % ans_template)
            
            return ans_template

        else:
            sys.stderr.write("Warning: System can only handle \"factoid\" questions\n")



    # This method takes as input a list of tokens (strings) and returns a 2-tuple in which
    # the first element is a list of the tokens that are not named entities (strings) and
    # the second element is a list of the named entities (strings).

    def extract_ne(self, input):
#       sys.stderr.write("DEBUG QUERY_PROCESSING.EXTRACT_NE()  Here is the input: %s\n" % input)

        # phrases in quotation marks are NEs, let's treat them as such
        possible_ne = []
        in_ne = False

        for word in input:
            if word == "''" and in_ne:
                in_ne = False
                possible_ne.append(current_ne.strip())
            if in_ne:
                current_ne = current_ne + " " + word
            if word == '``' and not in_ne:
                in_ne = True
                current_ne = ''

        #if len(possible_ne) > 0:
        #    sys.stderr.write("DEBUG: Here are the quoted possible NEs: "+str(possible_ne)+"\n")
        
        ne = possible_ne
        non_ne = input
        
        pos_tagged = nltk.pos_tag(input)
        extracted = nltk.ne_chunk(pos_tagged, binary=True)
        # find NE-headed subtrees
        for subtree in extracted.subtrees(lambda t: t.node == "NE"):
            leaves = subtree.leaves()
            # add space-delimited NE phrases to ne list
            current_ne = ' '.join(leaf[0] for leaf in leaves)
            ne.append(current_ne)
            # note: this isn't foolproof, but should work for now. I can't figure out how to get
            # the indices of the NE terms in the surface string -Clara
            #for leaf in leaves:
                #sys.stderr.write("trying to remove "+leaf[0]+" from "+str(non_ne)+"\n")
            #    non_ne.remove(leaf[0])

        for entity in possible_ne:
            entity_split = entity.split()
            if len(entity_split) > 1:
                for word in entity_split:
                    if word in ne:
                        ne.remove(word)

        for entity in ne:
            entity_split = entity.split()
            for word in entity_split:
                if word in non_ne:
                    non_ne.remove(word)

        # deduplicate ne
        # because may have same one word NE from quoted phrase and from NLTK
        ne = list(set(ne))
        
        #sys.stderr.write("DEBUG QUERY_PROCESSING.EXTRACT_NE()  Here is the list of non-named entities: %s\n" % non_ne)
        #sys.stderr.write("DEBUG QUERY_PROCESSING.EXTRACT_NE()  Here is the list of named entities: %s\n" % ne)

        non_ne_pos_tagged = []
        for pair in pos_tagged:
            if pair[0] in non_ne:
                non_ne_pos_tagged.append(pair)
        
#       sys.stderr.write("DEBUG  Here are the non-named entities: %s\n" % non_ne)
#       sys.stderr.write("DEBUG  Here are the POS-tagged non-named entities: %s\n" % non_ne_pos_tagged)
        
        return non_ne, ne, non_ne_pos_tagged
