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
	# script needs to have passed in: path to TREC question file, path to index
	# first argument is the TREC question file
	q_file = open(sys.argv[1],'r')
	# second argument is the index path
	index_path = sys.argv[2]
	# should the output file be a third argument?
	# or should we output the stdout?

	# comments taken from our shared Google Doc
	# instantiate an InfoRetriever using a set of documents
	# actually, no need, index is stored in set location, InfoRetriever can access it there
	# instead, index document collection

	# do XML stripping of TREC question file
	questions = generate_q_list(q_file)
	q_file.close()
	
	# filter for only factoid questions
	questions = filter(lambda x: x.type=='FACTOID', questions)

	# for a given Question object:
	for question in questions:

		# instantiate a QueryProcessor and use to generate a set of searches and an AnswerTemplate object
		qp = QueryProcessor(question)

		# use the InfoRetriever and the search set to generate a set of passages

		# instantiate an AnswerProcessor that takes set of passages and the AnswerTemplate object and returns a ranked list of answers

		# do formatting on answer list
		



# This method takes an XML file of questions as input, creates relevant Question objects,
# and returns them in a list.

def generate_q_list(xml_file):
	# parse the xml file (using Beautiful Soup?)
	# create relevant Question objects from the parse tree
	# return the Question objects in a sequential list

	soup = BeautifulSoup(xml_file)

	soup_targets = soup.find_all('target')
	questions = []
	
	for soup_target in soup_targets[:1]:
		target = soup_target.get('text')
		soup_questions = soup_target.find_all('q')

		for soup_question in soup_questions:
			id = soup_question.get('id')
			type = soup_question.get('type')
			q = soup_question.get_text().strip()
			question = Question(id, type, q, target)
			questions.append(question)
	return questions


if __name__ == '__main__':
	main()
