#!/bin/sh

# Tell the script what directory it's in
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the question-answering Python wrapper, passing all arguments to this shell script
$DIR/question_answering.py $@

# Run the MRR eval script with strict evaluation, redirecting output to the appropriate results file
tython2.6 /dropbox/13-14/573/code/compute_mrr.py /dropbox/13-14/573/Data/patterns/devtest/factoid-docs.litkowski.2006.txt $4 strict > $DIR/../results/test/results_strict

# Run the MRR eval script with lenient evaluation, redirecting output to the appropriate results file
python2.6 /dropbox/13-14/573/code/compute_mrr.py /dropbox/13-14/573/Data/patterns/devtest/factoid-docs.litkowski.2006.txt $4 lenient > $DIR/../results/test/results_lenient



