# LING 573 Question Answering System
# Code last updated 5/2/14 by Clara Gordon
# This code implements an InfoRetriever for the question answering system.


import pymur
from general_classes import *
import sys
import nltk
from bs4 import BeautifulSoup
import requests
import math
import base64

class InfoRetriever:

    # This method builds a QueryEnvironment associated with the indexed document collection.
    
    def __init__(self, parameters):
        self.path_to_idx = parameters['index']
        self.index = pymur.Index(self.path_to_idx)
        self.query_env = pymur.QueryEnvironment()
        self.query_env.addIndex(self.path_to_idx)
        self.indri_passages = int(parameters['indri_passages'])
        self.passage_length = parameters['passage_length']
        self.indri_window_size = parameters['indri_window_size']
        
        


    # This method takes a collection of SearchQuery objects as input and returns a list
    # of all the Passage objects returned by all the queries.
    
    def retrieve_passages(self, queries):
        passages = []
        for query in queries:
            if query.weight != 0:
                passages.extend(self.trec_passages(query))
                #passages.extend(self.web_search(query))
        return passages


    # This method takes a SearchQuery object as input and returns a list of related Passage
    # objects returned by Indri.
    
    def trec_passages(self, query):
        # generate string of weights followed by terms
        query_str = ""
        for term in query.search_terms.keys():
            query_str += str(query.search_terms[term]) + ' #1(#base64(' + base64.b64encode(term) + ')) ' 	
       
        passages = []
        #sys.stderr.write(query_str + '\n')
      	sys.stderr.write('Running query: ' + str(query.search_terms.keys()) + '\n')

	
	indri_query = "#weight[passage" + self.passage_length + ":" + self.indri_window_size + "](" + query_str + ")"
        
	try:
	    docs = self.query_env.runQuery(indri_query, self.indri_passages)
        except:
            docs = []
            sys.stderr.write("Couldn't run query: " + indri_query + '\n')
        for doc in docs:
            doc_num = doc.document
            begin = doc.begin
            end = doc.end

            orig_doc  = self.query_env.documents([doc_num])[0] # need this for output
            doc_id  = orig_doc.metadata['docno']

            orig_text = " ".join([x for x in orig_doc.text.split("<TEXT>")[1].split() if "<" not in x])
            passage_text = ' '.join(nltk.word_tokenize(orig_text)[begin:end])
            print "passage text", passage_text
	    # passage weight transformation happens here
            passage = Passage(passage_text, query.weight*(-doc.score**-1), doc_id)
            passages.append(passage)
        return passages
    
    
    # This method takes a SearchQuery object as an argument, queries ask.com for web snippets,
    # and returns the web snippets (Passage objects) in a list.
    # This method is no longer called, as web results are being cached ahead of time and
    # accessed in the shell script.
            
    def web_search(self, query):

        p_snippets = []
        results = []
        query_url = '+'.join(query.search_terms.keys())
        r = requests.get("http://www.ask.com/web?q=" + query_url)
        data = r.text
        soup = BeautifulSoup(data)
        for p in soup.find_all('p'):
            if 'class' in p.attrs.keys():
                if p['class'] == ['abstract', 'txt3']:
                    p_snippets.append(p.get_text().encode('utf-8'))

        for snippet in p_snippets:
            results.append(Passage(snippet, math.log(0.9), None))

        if not results:
            sys.stderr.write("No web search results for query: "+query_url+"\n")

        return results



# nltk.word_tokenize(" ".join([x for x in doc.text.split("<TEXT>")[1].split() if "<" not in x]))[begin:end]
# would be better w/ XML parsing (use BeautifulSoup), take out "TEXT" attributes, get rid of <P> </P>??
