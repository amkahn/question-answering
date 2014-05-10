#!/opt/python-2.7/bin/python2.7
#
# script can be run without invoking python because of shebang
# will be run with correct version on Patas
#
# LING 573 Question Answering System
# Code last updated on 5/5/14 by Claire Jaja
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
import multiprocessing
from functools import partial
from collections import defaultdict


def main():
	# first argument is the path to the TREC question file
    q_file = open(sys.argv[1],'r')
	
	# second argument is the path to the document index
    index_path = sys.argv[2]

    # third argument is web cached results for the questions
    web_cache = open(sys.argv[3],'r')

    # fourth argument is the run tag
    run_tag = sys.argv[4]

    # fifth argument is the path to the output file
    output = open(sys.argv[5],'w')

    quail = Quail(q_file, index_path, web_cache)

    questions = quail.generate_q_list()
	# filter for only factoid questions
    questions = filter(lambda x: x.type=='FACTOID', questions)

    partial_process_question = partial(process_question, object=quail)
    pool = multiprocessing.Pool()
    all_answers = pool.map(partial_process_question,questions)

    # do formatting on answer list
    for ranked_answers in all_answers:
        for answer in ranked_answers:
            #sys.stderr.write("DEBUG: Answer %s with score %s\n" % (answer.answer, answer.score))
            #sys.stderr.write("DEBUG: Answer %s found in: %s\n" % (answer.answer, answer.doc_ids))
            doc_id = next(iter(answer.doc_ids))
            output.write("%s %s %s %s\n" % (answer.question_id, run_tag, doc_id, answer.answer))
    output.close()


# This method takes an XML file of stopwords as input and returns a list of the stopwords.
def extract_stopwords(stopword_file):
    stopword_list = set()
    parsed_stopword_file = BeautifulSoup(stopword_file)
    stopwords = parsed_stopword_file.find_all("word")
    for stopword in stopwords:
        stopword_list.add(str(stopword.get_text()))
    return stopword_list


# This method takes a question and a question-answering object
# and runs the question through the question-answering pipeline.
def process_question(question,object):
    ranked_answers = object.process_question(question)
    return ranked_answers



# A Quail object has attributes q_file (a path to a TREC question file), index_path (a path
# to a document index), and cached_results (a path to a file of cached web results).
# It contains methods for generating a list of questions from the TREC question file, processing
# the web cache, and processing individual questions.

class Quail:
    def __init__(self,q_file,index_path, web_cache):
        self.q_file = q_file
        self.index_path = index_path
        self.cached_results = self.process_web_cache(web_cache)

        # path to the directory containing this script, so it can be run by scripts in other directories
        self.dir = path.dirname(__file__)

        # stopword list
        stopword_filename = path.join(self.dir, "stoplist.dft")
        stopword_file = open(stopword_filename)
        self.stopword_list = extract_stopwords(stopword_file)
        #sys.stderr.write("Stop words are: "+str(stopword_list))

    	# NB: indexing of document collection happens in separate script


    # This method takes an XML file of questions as input, creates relevant Question objects,
    # and returns them in a list.
    
    def generate_q_list(self):
	    # parse the xml file using BeautifulSoup
    	# create relevant Question objects from the parse tree
	    # return the Question objects in a sequential list

        soup = BeautifulSoup(self.q_file)

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
        self.q_file.close()
        return questions

    
    # This method reads in a web cache file and stores it in a dictionary.
    # It returns a dictionary where the key is the question ID
    # and the value is a list of web search snippets.
    def process_web_cache(self,web_cache):
        cached_results = defaultdict(list)
        for line in web_cache:
            line = line.strip()
            if line.startswith("QUESTION ID:"):
                question_id = line.split()[-1]
            elif line:
                cached_results[question_id].append(line)

        return cached_results


    # This method runs the question answering pipeline on a single question.
    # It returns a ranked list of AnswerCandidate objects.
    def process_question(self,question):
        #sys.stderr.write("\nDEBUG  Here is the question: %s\n" % question.to_string())

	    # instantiate a QueryProcessor and use it to generate a set of searches and an AnswerTemplate object
        qp = QueryProcessor(question)
		
        search_queries = qp.generate_queries()
        #sys.stderr.write("DEBUG  Here are the search queries: %s\n" % search_queries)

        ans_template = qp.generate_ans_template()
        #sys.stderr.write("DEBUG  Here is the answer template: %s\n" % ans_template.to_string())

        # use the InfoRetriever, the document index, and the search queries to generate a set of passages
        ir = InfoRetriever(self.index_path)
        
        passages = ir.retrieve_passages(search_queries)
        #sys.stderr.write("DEBUG  Here are the passages: \n")
        #for passage in passages:
        #    sys.stderr.write(passage.to_string()+"\n")

        # add web cached results to passages
        for cached_result in self.cached_results[question.id]:
            passages.append(Passage(cached_result, math.log(0.9), None))

       	# instantiate an AnswerProcessor that takes set of passages and the AnswerTemplate object
        ap = AnswerProcessor(passages,ans_template,self.stopword_list)

        # get a ranked list of answers
        ranked_answers = ap.generate_and_rank_answers()

        return ranked_answers



if __name__ == '__main__':
	main()
