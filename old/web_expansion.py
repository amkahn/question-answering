import sys
import nltk
from nltk.text import *
import re
#from general_classes import *
from collections import defaultdict
#from nltk.corpus import lin_thesaurus as thes
import heapq
#from copy import deepcopy
from nltk.collocations import *


def process_web_cache(web_cache):
	cached_results = defaultdict(list)
	for line in web_cache:
		line = line.strip()
		if line.startswith("QUESTION ID:"):
			question_id = float(line.split()[-1])
		elif line != '':
			cached_results[question_id].append(line)
	return cached_results



# Takes a list of strings corresponding to the web snippets, 
# a parameter for the number of top unigrams to return, and a
# list of stopwords.
# Returns a list of most frequent unigrams.
def web_expansion_frequency(snippets, n, stoplist, query):
	
	dict = defaultdict(int)

	for snippet in snippets:
		for token in snippet.lower().replace('...', ' ').split():
			if not token in stoplist and not token in query:
				dict[token] += 1

	return heapq.nlargest(n, dict, key = lambda k: dict[k])




# Takes a list of strings corresponding to the web snippets, 
# and a parameter for the number of top unigrams to return.
# Returns a list of top bigram collocations.
def web_expansion_collocations(snippets, n):

	dict = defaultdict(int)
	tokens = ''
	ranked_unigrams = {}
	texts = []


	bigram_measures = nltk.collocations.BigramAssocMeasures()
	trigram_measures = nltk.collocations.TrigramAssocMeasures()

	_temp = ''
	for line in snippets:
	
		line = line.strip().replace('...', ' ')
		_temp += line + ' '
		for token in line.split(' '):
			dict[token] += 1
		texts.append(Text(line))	

	finder = BigramCollocationFinder.from_words(_temp)
	finder = BigramCollocationFinder.from_words(
			   nltk.corpus.genesis.words('english-web.txt'))


	#collection = TextCollection(texts)
	#vocab = dict.keys()
	#for token in vocab:
	#	ranked_unigrams[token] = collection.tf_idf(token, vocab)


	#return heapq.nlargest(n, ranked_unigrams, key = lambda k: dict[k])
	
	#return the n  n-grams with the highest PMI
 	return finder.nbest(bigram_measures.pmi, n) 




# debugging code
def main():
	web_cache = process_web_cache(open('../cached_web_results/TREC-2006.3pg.web_cache', 'r'))
	print web_expansion_frequency(web_cache[141.5], 10, ['a', 'the', 'he', 'to', 'of'], ['warren', 'moon'] )

	#print web_unigrams(['this is a test', 'this is another test', 'this is the last test'], 3)

main()



