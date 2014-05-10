#!/opt/python-2.7/bin/python2.7
#
# script can be run without invoking python because of shebang
# will be run with correct version on Patas
#
# LING 573 Question Answering System
# Code last updated on 5/9/2014 by Claire Jaja
#
# This script will retrieve and cache web results for all the questions in the test set.
# It waits 1 second between queries to avoid being throttled.


import sys
import time
from general_classes import *
from bs4 import BeautifulSoup
import requests
import re

def main():
	# first argument is the TREC question file
    q_file = open(sys.argv[1],'r')
	
	# second argument is the output file to cache the results
    cached_results = open(sys.argv[2],'w')

	# do XML stripping of TREC question file
    questions = generate_q_list(q_file)
    q_file.close()
	
	# filter for only factoid questions
    questions = filter(lambda x: x.type=='FACTOID', questions)

    # will store my snippets in a dictionary
    # key will be the question id
    # value will be a list of snippets
    web_snippets = {}
    #full_text = {}

    for question in questions:
        web_snippets[question.id] = []
        query = "+".join(question.target.split()) + "+" + "+".join(question.q.split())
        for i in range(1,5):
            r = requests.get("http://www.search.ask.com/web?q="+query+"&page="+str(i))
            data = r.text
            #full_text[question.id] = data.encode('utf-8')
            soup = BeautifulSoup(data)
            for element in soup.find_all('span',{'class':'nDesc'}):
                web_snippets[question.id].append(element.get_text().encode('utf-8'))
            time.sleep(1)


    for id, snippets in web_snippets.items():
        cached_results.write("QUESTION ID: "+str(id)+"\n")
        #cached_results.write("FULL TEXT: "+full_text[question.id]+"\n")
        for snippet in snippets:
            snippet = re.sub("\n"," ",snippet)
            cached_results.write(snippet+"\n")
        cached_results.write("\n")

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
