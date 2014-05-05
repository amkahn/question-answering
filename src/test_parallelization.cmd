question_file = /dropbox/13-14/573/Data/Questions/devtest/TREC-2006.xml
doc_index = /home2/cjaja/classwork/spring-2014/ling573/question-answering/src/indexes/index
run_tag = test_parallelization
output_file = ../outputs/test.parallelization.output

executable = question_answering_parallelized.py
arguments = $(question_file) $(doc_index) $(run_tag) $(output_file)
Universe = vanilla
getenv = true
output = test.parallelization.out
log = test.parallelization.log
error = test.parallelization.err
transfer_executable = false
request_memory = 1024
queue
