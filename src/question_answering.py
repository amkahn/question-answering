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


# This method reads in command line arguments and stores them in a dict. It 
# assigns default values if none are specified. 

def get_parameters(args, script_dir):
    
    
    if len(args) == 0:
        raise Exception('Must include runtag as first argument.')

    if '=' in args[0]:
        raise Exception('First argument must be run tag only.')

    parameters = {'run_tag':args[0]}

    for arg in args[1:]:
        split = arg.split('=')
        if len(split) == 2:
            parameters[split[0]] = split[1]
        else:
            sys.stderr.write('Ill-formed parameter: ' + arg)


    # CODE FOR DEFAULT PARAMETER VALUES HERE
    
    keys = parameters.keys()
    
    # Wrapper script parameters
    if 'q_file' not in keys:
        parameters['q_file'] = '/dropbox/13-14/573/Data/Questions/devtest/TREC-2006.xml'    
            
    if 'stoplist' not in keys:
        parameters['stoplist'] = script_dir + '/stoplist.dft'
        
    if 'web_cache' not in keys:
        parameters['web_cache'] = script_dir + '/cached_web_results/TREC-2006.3pg.web_cache'
    
    if 'index' not in keys:
        parameters['index'] = '/home2/cjaja/classwork/spring-2014/ling573/question-answering/src/indexes/index.porter.stoplist'

    # Query processing parameters
    if 'stopword_filter_target' not in keys:
        parameters['stopword_filter_target'] = False
    
    if 'target_upweighting' not in keys:
        parameters['target_upweighting'] = '1'

    if 'ne_upweighting' not in keys:
        parameters['ne_upweighting'] = '1'
    
    if 'num_web_exp_terms' not in keys:
        parameters['num_web_exp_terms'] = '5'

    if 'weight_web_exp_terms' not in keys:
        parameters['weight_web_exp_terms'] = '0.5'

    if 'num_lin_exp_terms' not in keys:
        parameters['num_lin_exp_terms'] = '0'
            
    if 'weight_lin_exp_query' not in keys:
        parameters['weight_lin_exp_query'] = '0'
    
    # IR parameters
    if 'indri_passages' not in keys:
        parameters['indri_passages'] = '40'
    
    if 'passage_length' not in keys:
        parameters['passage_length'] = '100'
        
    if 'snippet_weight' not in keys:
        parameters ['snippet_weight'] = '0.9'
        
    if 'indri_window_size' not in keys:
        parameters['indri_window_size'] = '50'

    # Answer processing parameters
    if 'num_docs' not in keys:
        parameters['num_docs'] = '1'

    if 'num_passages' not in keys:
        parameters['num_passages'] = '10'

    if 'snippet_passage_count' not in keys:
        parameters['snippet_passage_count'] = '10'

    if 'passages_per_doc_id' not in keys:
        parameters['passages_per_doc_id'] = '1'

    if 'passages_per_answer_candidate' not in keys:
        parameters['passages_per_answer_candidate'] = '1'

    return parameters


def main():

    script_dir = path.dirname(path.realpath(__file__))
    
    # pass arguments to get_parameters method 
    sys.stderr.write('Getting parameters...\n')
    parameters = get_parameters(sys.argv[1:], script_dir)
    sys.stderr.write('Parameters: ' + str(parameters) + '\n')

    # read run tag and output from parameters dict
    run_tag = parameters['run_tag']
    output = open(script_dir + '/../outputs/' + run_tag + '.outputs','w')
          
    quail = Quail(parameters)

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
            question_id, doc_id, passage = answer

            output.write("%s %s %s %s\n" % (question_id, run_tag, doc_id, passage))
    output.close()


# This method takes an XML file of stopwords as input and returns a list of the stopwords.

def extract_stopwords(stopword_file):
    stopword_list = set()
    parsed_stopword_file = BeautifulSoup(stopword_file)
    stopwords = parsed_stopword_file.find_all("word")
    for stopword in stopwords:
        stopword_list.add(str(stopword.get_text()))
    return stopword_list


# This method takes a question and a question-answering object and runs the question through
# the question-answering pipeline.

def process_question(question,object):
    ranked_answers = object.process_question(question)
    return ranked_answers



# A Quail object has attributes q_file (a path to a TREC question file), index_path (a path
# to a document index), and cached_results (a path to a file of cached web results).
# It contains methods for generating a list of questions from the TREC question file, processing
# the web cache, and processing individual questions.

class Quail:
    def __init__(self, parameters):
    
        self.parameters = parameters

        # path to the TREC question file
        self.q_file = open(self.parameters['q_file'],'r')
        
        # path to the document index
        self.index_path = self.parameters['index']
        
        # web cached results for the questions
        self.cached_results = self.process_web_cache(open(self.parameters['web_cache'],'r'))

        # path to the directory containing this script, so it can be run by scripts in other directories
        self.dir = path.dirname(__file__)

        # stopword list
        stopword_file = open(self.parameters['stoplist'])
        self.stopword_list = extract_stopwords(stopword_file)
        #sys.stderr.write("Stop words are: "+str(stopword_list))

        # snippet weight
        self.snippet_weight = float(self.parameters['snippet_weight'])

        
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
                id = str(soup_question.get('id'))
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
                question_id = float(line.split()[-1])
            elif line != '':
                cached_results[question_id].append(line)

        return cached_results


    # This method runs the question answering pipeline on a single question.
    # It returns a ranked list of AnswerCandidate objects.
    
    def process_question(self,question):
        #sys.stderr.write("\nDEBUG  Here is the question: %s\n" % question)

        # instantiate a QueryProcessor and use it to generate a set of searches and an AnswerTemplate object
        qp = QueryProcessor(self.parameters, question, self.stopword_list, self.cached_results[question.id])
        
        search_queries = qp.generate_queries()
        #sys.stderr.write("DEBUG  Here are the search queries: %s\n" % search_queries)

        ans_template = qp.generate_ans_template()
        #sys.stderr.write("DEBUG  Here is the answer template: %s\n" % ans_template)

        # use the InfoRetriever, the document index, and the search queries to generate a set of passages
        ir = InfoRetriever(self.parameters)
        
        passages = ir.retrieve_passages(search_queries)
        #sys.stderr.write("DEBUG  Here are the passages: \n")
        #for passage in passages:
        #    sys.stderr.write(passage+"\n")

        # add web cached results to passages -- score inside log can be adjusted accordingly
        #sys.stderr.write("Adding "+str(len(self.cached_results[question.id]))+" web result passages for "+str(question.id)+"\n")
        for cached_result in self.cached_results[question.id]:
            passages.append(Passage(cached_result, -math.log(self.snippet_weight)**-1, None))

        # instantiate an AnswerProcessor that takes set of passages and the AnswerTemplate object
        ap = AnswerProcessor(passages,ans_template,self.stopword_list,self.parameters)

        # get a ranked list of answers
        ranked_answers = ap.generate_and_rank_answers()

        return ranked_answers



if __name__ == '__main__':
    main()
