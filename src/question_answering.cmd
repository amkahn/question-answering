question_file = /dropbox/13-14/573/Data/Questions/devtest/TREC-2006.xml
doc_index = /home2/cjaja/classwork/spring-2014/ling573/question-answering/src/index

executable = question_answering.py
arguments = $(question_file) $(doc_index)
Universe = vanilla
getenv = true
output = test.out
log = test.log
error = test.err
transfer_executable = false
request_memory = 1024
queue