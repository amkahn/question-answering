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
	# script needs to have passed in: path to documents, path to TREC question file
	# first argument is the folder with the document collection
	# for the AQUAINT corpus, this is "/corpora/LDC/LDC02T31"
	document_collection = sys.argv[1]
	# second argument is the TREC question file
	questions = open(sys.argv[2],'r')
	# should the output file be a third argument?
	# or should we output the stdout?

	# comments taken from our shared Google Doc
	# instantiate an InfoRetriever using a set of documents
	# actually, no need, index is stored in set location, InfoRetriever can access it there
	index_documents(document_collection)

	# for a given TREC file
		# do XML stripping (use package?), filter for only factoid questions
		# generate Question objects (incrementally as it feeds them to the pipeline? or all at once?)
		# for a given Question object
			# instantiate a QueryProcessor and use to generate a set of searches and an AnswerTemplate object
			# use the InfoRetriever and the search set to generate a set of passages
			# instantiate an AnswerProcessor that takes set of passages and the AnswerTemplate object and returns a ranked list of answers
			# do formatting on answer list

def index_documents(document_collection):
	# the document collection is a folder
	# first, find the subfolders (these correspond to document sources)
	# we don't want to start looking for files here because there are documentation files
	document_folders = [ path.join(document_collection,x) for x in listdir(document_collection) if path.isdir(path.join(document_collection,x)) ]
	# then find all the documents by traversing document folders
	all_documents = []
	for document_folder in document_folders:
		for (dirpath, dirnames, filenames) in walk(document_folder):
			all_documents.extend(path.join(dirpath,filename) for filename in filenames)

	# for now this is taken from http://findingscience.com/pymur/examples.html
	i = IndexEnvironment()

	# use 1000 bytes - I'm guessing we'll actually need more?
	i.setMemory(1000) 

	# do normalize - this performs case normalization - we probably want it
	i.setNormalization(True)

	# set stemmer
	# two possible stemmers - "porter" (overgeneralizes), "krovetz" (doesn't overgeneralize)
	# indri/lemur doc says this is optional, so I think we can just omit to not stem
	i.setStemmer("porter")

	# make sure that the metadata we just added is indexed and searchable
	# we will make sure "title" is indexed for both forward and backward searches
	# is this the place to make sure we'll be able to access doc IDs?
	i.setMetadataIndexedFields(["title"], ["title"])

	# make index - the InfoRetriever can access this by knowing the path
	i.create("./index")

	# add files
	for document in all_documents:
		print("Adding file: "+document) # for testing purposes
		i.addFile(document, "trectext") # untested, I think this is the correct format

	i.close()

main()
