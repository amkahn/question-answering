#!/opt/python-2.7/bin/python2.7
#
# script can be run without invoking python because of shebang
# will be run with correct version on Patas
#
# LING 573 Question Answering System
# Code last updated on 4/22/14 by Andrea Kahn
#
# This is the wrapper script.


import sys
import time
from general_classes import *
from query_processing.query_processing import *
from info_retrieval.info_retrieval import *
from answer_processing.answer_processing import *
from pymur import *
from bs4 import BeautifulSoup
from os import listdir, path, walk


def main():
	# first argument is the TREC question file
    q_file = open(sys.argv[1],'r')
	
	# second argument is the path to the index
    index_path = sys.argv[2]

	# should the output file be a third argument?
	# or should we output the stdout?
    output = sys.stdout

    # run-tag for output file - maybe later add as fourth argument?
    run_tag = "test"

    # Keep track of the total time required for some processes.
    query_gen_time = 0
    ans_temp_gen_time = 0
    ir_time = 0
    ans_gen_time = 0

	# NB: indexing of document collection happens in separate script

	# do XML stripping of TREC question file
    questions = generate_q_list(q_file)
    q_file.close()
	
	# filter for only factoid questions
    questions = filter(lambda x: x.type=='FACTOID', questions)

	# for a given Question object:
    for question in questions:
#       sys.stderr.write("\nDEBUG  Here is the question: %s\n" % question.to_string())

		# instantiate a QueryProcessor and use it to generate a set of searches and an AnswerTemplate object
        qp = QueryProcessor(question)
		
        begin_query_gen = time.clock()
        search_queries = qp.generate_queries()
        end_query_gen = time.clock()
        query_gen_time += (end_query_gen - begin_query_gen)
#       sys.stderr.write("DEBUG  Here are the search queries: %s\n" % search_queries)
#       sys.stderr.write("DEBUG  Generating the search queries took %s seconds\n" % (end_query_gen - begin_query_gen))

        begin_ans_temp_gen = time.clock()
        ans_template = qp.generate_ans_template()
        end_ans_temp_gen = time.clock()
        ans_temp_gen_time += (end_ans_temp_gen - begin_ans_temp_gen)
#       sys.stderr.write("DEBUG  Here is the answer template: %s\n" % ans_template.to_string())
#       sys.stderr.write("DEBUG  Generating the answer template took %s seconds\n" % (end_ans_temp_gen - begin_ans_temp_gen))

   		# use the InfoRetriever, the document index, and the search queries to generate a set of passages
        ir = InfoRetriever(index_path)
        
        begin_ir = time.clock()
        passages = ir.retrieve_passages(search_queries)
        end_ir = time.clock()
        ir_time += (end_ir - begin_ir)
        sys.stderr.write("DEBUG  Here are the passages: %s\n")
        for passage in passages:
            sys.stderr.write(passage.to_string()+"\n")
        sys.stderr.write("DEBUG  Passage retrieval took %s seconds\n" % (end_ir - begin_ir))
        
        # dummy set of passage objects to test AnswerProcessor
        # passages = []
        # for i in range(20):
        #     passage = Passage("this is a test",i,"NYT123"+str(i))
        #     passages.append(passage)
        # dummy answer template to test AnswerProcessor
        # ans_template = AnswerTemplate("what are you doing?")

   		# instantiate an AnswerProcessor that takes set of passages and the AnswerTemplate object
        ap = AnswerProcessor(passages,ans_template)

        # get a ranked list of answers
        begin_ans_gen = time.clock()
        ranked_answers = ap.generate_and_rank_answers()
        end_ans_gen = time.clock()
        ans_gen_time += (end_ans_gen - begin_ans_gen)
        sys.stderr.write("DEBUG  Generating and reranking answers took %s seconds\n" % (end_ans_gen - begin_ans_gen))

		# do formatting on answer list
        for answer in ranked_answers:
            output.write("%s %s %s %s\n" % (question.id, run_tag, answer.doc_id, answer.answer))

    sys.stderr.write("Query generation took %s seconds\n" % query_gen_time)
    sys.stderr.write("Answer template generation took %s seconds\n" % ans_temp_gen_time)
    sys.stderr.write("Passage retrieval took %s seconds\n" % ir_time)
    sys.stderr.write("Answer generation and ranking took %s seconds\n" % ans_gen_time)

# This method takes an XML file of questions as input, creates relevant Question objects,
# and returns them in a list.

def generate_q_list(xml_file):
	# parse the xml file using BeautifulSoup
	# create relevant Question objects from the parse tree
	# return the Question objects in a sequential list

	soup = BeautifulSoup(xml_file)

	soup_targets = soup.find_all('target')
	questions = []
	
	for soup_target in soup_targets:
		target = str(soup_target.get('text'))
		soup_questions = soup_target.find_all('q')

		for soup_question in soup_questions:
			id = float(soup_question.get('id'))
			type = str(soup_question.get('type'))
			q = str(soup_question.get_text().strip())
			question = Question(id, type, q, target)
			questions.append(question)
	return questions


if __name__ == '__main__':
	main()
