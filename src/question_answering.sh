#!/bin/sh

# This script takes as arguments:
#   1) the path to the TREC question file
#   2) the path to the document index
#   3) the cached web search results for the question file
#   4) the run-tag
#   5) the path to the output file
#   6) the first portion of the filename for the results file
#
# It runs the Python question-answering wrapper script, then runs the MRR eval script with strict
# and lenient evaluation, respectively.


# Tell the script what directory it's in
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the question-answering Python wrapper, passing first five arguments to this shell script
$DIR/question_answering.py $1 $2 $3 $4 $5

# Run the MRR eval script with strict evaluation, redirecting output to the appropriate results file
python2.6 /dropbox/13-14/573/code/compute_mrr.py /dropbox/13-14/573/Data/patterns/devtest/factoid-docs.litkowski.2006.txt $5 strict > $DIR/../results/$6.results_strict

# Run the MRR eval script with lenient evaluation, redirecting output to the appropriate results file
python2.6 /dropbox/13-14/573/code/compute_mrr.py /dropbox/13-14/573/Data/patterns/devtest/factoid-docs.litkowski.2006.txt $5 lenient > $DIR/../results/$6.results_lenient
