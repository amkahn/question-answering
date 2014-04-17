#!/opt/python-2.7/bin/python2.7
# script can be run without invoking python because of shebang
# will be run with correct version on Patas
# LING 573 Question Answering System
# Last edited on 4/17/14 by Andrea Kahn
#
# This is the wrapper script.


import sys
from general_classes import *
from query_processing.query_processing import *
from info_retrieval.info_retrieval import *
from answer_processing.answer_processing import *
# from lxml import etree
from pymur import *
from os import listdir, path, walk


def main():
	# script needs to have passed in:
	# path to documents, path to TREC question file, optionally path to output file

	# first argument is the folder with the document collection
	# for the AQUAINT corpus, this is "/corpora/LDC/LDC02T31"
	document_collection = sys.argv[1]

	# second argument is the TREC question file
	q_file = open(sys.argv[2],'r')
	
	# should the output file be a third argument?
	# or should we output the stdout?

	# comments taken from our shared Google Doc
	# instantiate an InfoRetriever using a set of documents
	# actually, no need, index is stored in set location, InfoRetriever can access it there
	# instead, index document collection
	index_documents(document_collection)

	# do XML stripping (use package?), filter for only factoid questions
	questions = generate_q_list(q_file)
	questions = filter(lambda x: x.type=='factoid', questions)

	# for a given Question object:
	for question in questions:

		# instantiate a QueryProcessor and use to generate a set of searches and an AnswerTemplate object
		qp = QueryProcessor(question)

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


# FIXME: incomplete/untested code; for now, this method simply returns a dummy list of
# Question objects so that the program can be run.

# This method takes an XML file of questions as input, creates relevant Question objects,
# and returns them in a list.

def generate_q_list(xml_file):
#	parsed_file = etree.parse(xml_file)	# use beautiful soup instead? (which sits on top of lxml)
	# may need to first get rid of junk at the beginning/end of the file
	# then, parse the xml file (using Beautiful Soup?)
	# create relevant Question objects from the parse tree
	# return the Question objects in a sequential list

	q1 = Question(None, 'factoid', None, None)
	q2 = Question(None, 'description', None, None)
	return [q1, q2]


if __name__ == '__main__':
	main()