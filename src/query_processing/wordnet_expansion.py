from nltk.corpus import wordnet as wn









def expand_query(query):
	
	
	weighted_query_terms = {}
	
	q_length = len(query)
	
	for i in range (0, q_length):
		for j in range (i, q_length):
		 	print get_synset_similarity(query[i], query[j])



def get_synset_similarity(t1, t2):
	"""
	takes a pair of query terms and returns their synset similarity: the 
	overlap between the glosses of all the synsets of both terms
	"""

	overlap = (get_synset_glosses(t1).intersection(get_synset_glosses(t2)))
	print overlap
	return overlap, len(overlap)



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


