question_file = /dropbox/13-14/573/Data/Questions/devtest/TREC-2006.xml
doc_index = /home2/cjaja/classwork/spring-2014/ling573/question-answering/src/indexes/index
run_tag = test_web_boost
output_file = ../outputs/test.web_boost.output

executable = question_answering_parallelized.py
arguments = $(question_file) $(doc_index) $(run_tag) $(output_file)
Universe = vanilla
getenv = true
output = test.web_boost.out
log = test.web_boost.log
error = test.web_boost.err
transfer_executable = false
request_memory = 1024
queue
