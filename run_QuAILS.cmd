question_file = /dropbox/13-14/573/Data/Questions/devtest/TREC-2006.xml
doc_index = /home2/cjaja/classwork/spring-2014/ling573/question-answering/src/indexes/index.porter.stoplist
run_tag = index.porter.stoplist
output_file = outputs/index.porter.stoplist.out
results_file = $(run_tag)

executable = src/question_answering.sh
arguments = $(question_file) $(doc_index) $(run_tag) $(output_file) $(results_file)
Universe = vanilla
getenv = true
output = D2.out
log = D2.log
error = D2.err
transfer_executable = false
request_memory = 1024
Queue

doc_index = /home2/cjaja/classwork/spring-2014/ling573/question-answering/src/indexes/index.krovetz.stoplist
run_tag = index.krovetz.stoplist
output_file = outputs/index.krovetz.stoplist.out
results_file = $(run_tag)
Queue

doc_index = /home2/cjaja/classwork/spring-2014/ling573/question-answering/src/indexes/index.none.stoplist
run_tag = index.none.stoplist
output_file = outputs/index.none.stoplist.out
results_file = $(run_tag)
Queue
