from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
semcor_ic = wordnet_ic.ic('ic-semcor.dat')
from nltk.corpus import lin_thesaurus as thes
import heapq

# specifies number of top-scoring synonyms to use
NUMBER_SYNONYMS = 3


def expand_query(query):
	
	# add weight of 1 for each original term
	weighted_terms = {}
	for term in query:
		weighted_terms[term] = 1

	# should do some stopword removal here

	for word in query:
		syns = thes.scored_synonyms(word)
		if (thes) > NUMBER_SYNONYMS:
			all_syns = []
			# syn list is in the form ((POS, [syn, syn, syn]), (POS, [syn, syn, syn]) ...)
			# concatenate all synonyms from the various lists 
			for element in syns:
				all_syns.extend(element[1])
			# get n-best synonyms according to Lin similarity
			top = heapq.nlargest(NUMBER_SYNONYMS, all_syns, key = lambda k: k[1])
		else:
			top = syns
		# add top synonyms to weighted term dict
		for element in top:
			weighted_terms[element[0]] = element[1]

	return weighted_terms


# functions below are old - probably won't want to use them

def get_synset_similarity(t1, t2):
	"""
	takes a pair of query terms and returns their synset similarity: the 
	overlap between the glosses of all the synsets of both terms
	"""

	overlap = (get_synset_glosses(t1).intersection(get_synset_glosses(t2)))
	print overlap
	return len(overlap)

def get_synset_glosses(t):
	"""
	returns a set of the glosses for each of a term's synsets
	"""

	glosses = set()
	for synset in wn.synsets(t):
		# not sure how to get glosses.. seems like a good approximation
		glosses.add(synset.lemma_names[0])

	return glosses
	

## debug code

get_synset_similarity("dog", "domestic_dog")


