# LING 573 Question Answering System
# Code last updated 4/17/14 by Clara Gordon
# This code implements an InfoRetriever for the question answering system.


from pymur import *
from general_classes import *
import sys


class InfoRetriever:


    # builds a QueryEnvironment associated with the indexed document collection
    def __init__(self, index_path):
        # how to get this to link up to the doc collection?

        self.path_to_idx = index_path
        self.index = Index(self.path_to_idx)
        self.query_env = QueryEnvironment()
        self.query_env.addIndex(self.path_to_idx)


    # creates a list of all the passages returned by all the queries generated by
    # the query-processing module
    def retrieve_passages(self, queries):
        passages = []
        for query in queries:
            query = " ".join(query.search_terms.keys())
            sys.stderr.write(query + '\n')
            # second argument is the number of documents desired
            try:
                docs = self.query_env.runQuery("#combine[passage50:25](" + query + ")", 20)
            except:
                docs = []
                sys.stderr.write("Couldn't run query: " + query + '\n')
            for doc in docs:
                doc_num = doc.document
                begin = doc.begin
                end = doc.end
                doc_id = self.query_env.documents([doc_num])[0].metadata['docno'] # need this for output
                passage = Passage(self.index.document(doc_num, True)[begin:end], doc.score, doc_id)
                passages.append(passage)

        return passages


