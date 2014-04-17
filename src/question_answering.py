#!/opt/python-2.7/bin/python2.7
# script can be run without invoking python because of shebang
# will be run with correct version on Patas
# LING 573 Question Answering System
# Last edited on 4/15/14 by Claire Jaja.
#
# This is the wrapper script.

import sys
from pymur import *
from os import listdir, path, walk

def main():
	# script needs to have passed in: path to TREC question file, path to index
	# first argument is the TREC question file
	questions = open(sys.argv[1],'r')
	# second argument is the index path
	index_path = sys.argv[2]
	# should the output file be a third argument?
	# or should we output the stdout?

	# comments taken from our shared Google Doc
	# instantiate an InfoRetriever using a set of documents
	# actually, no need, index is stored in set location, InfoRetriever can access it there

	# for a given TREC file
		# do XML stripping (use package?), filter for only factoid questions
		# generate Question objects (incrementally as it feeds them to the pipeline? or all at once?)
		# for a given Question object
			# instantiate a QueryProcessor and use to generate a set of searches and an AnswerTemplate object
			# use the InfoRetriever and the search set to generate a set of passages
			# instantiate an AnswerProcessor that takes set of passages and the AnswerTemplate object and returns a ranked list of answers
			# do formatting on answer list


main()
