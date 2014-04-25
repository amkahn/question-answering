#!/bin/sh

./question_answering.py $@

python2.6 /dropbox/13-14/573/code/compute_mrr.py /dropbox/13-14/573/Data/patterns/devtest/factoid-docs.litkowski.2006.txt $4 strict > ../results/D2.results_strict

python2.6 /dropbox/13-14/573/code/compute_mrr.py /dropbox/13-14/573/Data/patterns/devtest/factoid-docs.litkowski.2006.txt $4 lenient > ../results/D2.results_lenient