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

class InfoRetriever:


    # builds a QueryEnvironment associated with the indexed document collection
    def __init__(self, index_path):
        # how to get this to link up to the doc collection?

        self.path_to_idx = index_path
        self.index = pymur.Index(self.path_to_idx)
        self.query_env = pymur.QueryEnvironment()
        self.query_env.addIndex(self.path_to_idx)


    # creates a list of all the passages returned by all the queries generated by
    # the query-processing module
    def retrieve_passages(self, queries):
        passages = []
        web_results = []
        for query in queries:
            passages.extend(self.trec_passages(query))
            passages.extend(self.web_search(query))
        return passages


    def trec_passages(self, query):
        query = " ".join(query.search_terms.keys())
        passages = []
        #sys.stderr.write(query + '\n')
        # second argument is the number of documents desired
        try:
            docs = self.query_env.runQuery("#combine[passage100:50](" + query + ")", 100)
        except:
            docs = []
            sys.stderr.write("Couldn't run query: " + query + '\n')
        for doc in docs:
            doc_num = doc.document
            begin = doc.begin
            end = doc.end

            orig_doc  = self.query_env.documents([doc_num])[0] # need this for output
            doc_id  = orig_doc.metadata['docno']

            orig_text = " ".join([x for x in orig_doc.text.split("<TEXT>")[1].split() if "<" not in x])
            passage_text = ' '.join(nltk.word_tokenize(orig_text)[begin:end])
           # print "passage text", passage_text
            passage = Passage(passage_text, doc.score, doc_id)
            passages.append(passage)
        return passages
            
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

