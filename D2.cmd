question_file = /dropbox/13-14/573/Data/Questions/devtest/TREC-2006.xml
doc_index = /home2/cjaja/classwork/spring-2014/ling573/question-answering/src/index_krovetz
run_tag = D2
output_file = outputs/D2.outputs

executable = src/question_answering.sh
arguments = $(question_file) $(doc_index) $(run_tag) $(output_file)
Universe = vanilla
getenv = true
output = D2.out
log = D2.log
error = D2.err
transfer_executable = false
request_memory = 1024
queue
