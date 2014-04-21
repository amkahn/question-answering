# LING 573 Question Answering System
# Code last updated 4/17/14 by Clara Gordon
# This code implements an InfoRetriever for the question answering system.


# from pymur import *
from general_classes import *
import sys
import subprocess


class InfoRetriever:

    indri_loc = "/NLP_TOOLS/info_retrieval/indri/latest/bin/IndriRunQuery"

    # builds a QueryEnvironment associated with the indexed document collection
    def __init__(self, index_path):
        # how to get this to link up to the doc collection?

        self.path_to_idx = index_path


    # creates a list of all the passages returned by all the queries generated by
    # the query-processing module
    def retrieve_passages(self, queries):

        passages = []
        for query in queries:
            # query = " ".join(query.search_terms.keys())
            sys.stderr.write(query + '\n')
            # second argument is the number of documents desired
            try:
                p1 = subprocess.Popen([self.indri_loc, "".join("-index=", self.path_to_idx), \
                               "".join("-query=", '"#combine("', query,')"'), "-printSnippets=true"], \
                                      stdout=subprocess.PIPE, shell=True)
                results = (p1.communicate())
                print results
            except:
                sys.stderr.write("Couldn't run query: " + query + '\n')










