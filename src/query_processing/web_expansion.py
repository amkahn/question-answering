import sys
from nltk.text import *
import re
#from general_classes import *
from collections import defaultdict
#from nltk.corpus import lin_thesaurus as thes
import heapq
#from copy import deepcopy






# Takes a list of strings corresponding to the web snippets, 
# and a parameter for the number of top unigrams to return
# Returns a list of top unigrams.
def web_unigrams(snippets, n):

	dict = defaultdict(int)
	tokens = ''
	ranked_unigrams = {}
	texts = []


	for line in snippets:
		for token in line.split(' '):
			dict[token] += 1
		texts.append(Text(line))
	
	
	collection = TextCollection(texts)
	vocab = dict.keys()
	for token in vocab:
		ranked_unigrams[token] = collection.tf_idf(token, vocab)


	return heapq.nlargest(n, ranked_unigrams, key = lambda k: dict[k])




def main():
	
	print web_unigrams(['this is a test', 'this is another test', 'this is the last test'], 3)


main()



