#!/bin/sh

# First argument must be the run tag. All other arguments are optional, and identified
# using the format arg_type=arg_value.

# It runs the Python question-answering wrapper script, then runs the MRR eval script with strict
# and lenient evaluation, respectively.


# Tell the script what directory it's in
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the question-answering Python wrapper, passing first five arguments to this shell script
$DIR/question_answering.py $@

# Run the MRR eval script with strict evaluation, redirecting output to the appropriate results file
python2.6 /dropbox/13-14/573/code/compute_mrr.py /dropbox/13-14/573/Data/patterns/devtest/factoid-docs.litkowski.2006.txt $DIR/../outputs/QA.outputs_$1 strict > $DIR/../results/QA.results_$1_strict

# Run the MRR eval script with lenient evaluation, redirecting output to the appropriate results file
python2.6 /dropbox/13-14/573/code/compute_mrr.py /dropbox/13-14/573/Data/patterns/devtest/factoid-docs.litkowski.2006.txt $DIR/../outputs/QA.outputs_$1 lenient > $DIR/../results/QA.results_$1_lenient
