#!/opt/python-2.7/bin/python2.7
# script can be run without invoking python because of shebang
# will be run with correct version on Patas
# LING 573 Question Answering System
# Last edited on 4/17/14 by Claire Jaja.
#
# This script will index a document collection using Indri/Lemur.

import sys
from pymur import *
from os import listdir, path, walk

def main():
	# first argument is the folder with the document collection
	# for the AQUAINT corpus, this is "/corpora/LDC/LDC02T31"
	document_collection = sys.argv[1]
	# second argument is the folder to put the index in
	# WARNING: All contents of this folder will be deleted!
	index_folder = sys.argv[2]
	index_documents(document_collection,index_folder)

def index_documents(document_collection,index_folder):
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

	# use 2 MB
	i.setMemory(2000000) 

	# do normalize - this performs case normalization - we probably want it
	i.setNormalization(True)

	# set stemmer
	# two possible stemmers - "porter" (overgeneralizes), "krovetz" (doesn't overgeneralize)
	# indri/lemur doc says this is optional, so I think we can just omit to not stem
	i.setStemmer("krovetz")

	# make sure that the metadata we just added is indexed and searchable
	# we will make sure "title" is indexed for both forward and backward searches
	# I don't think we need this since "title" doesn't show up in our documents
    # and the trectext file adding automatically adds TREC fields
	#i.setMetadataIndexedFields(["title"], ["title"])

	# make index - the InfoRetriever can access this by knowing the path
	i.create(index_folder)

	# add files
	for document in all_documents:
		i.addFile(document, "trectext") # untested, I think this is the correct format

	i.close()

main()
