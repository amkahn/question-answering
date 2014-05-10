question_file = /dropbox/13-14/573/Data/Questions/devtest/TREC-2006.xml
doc_index = /home2/cjaja/classwork/spring-2014/ling573/question-answering/src/indexes/index.porter.stoplist
run_tag = index.porter.stoplist.2docIDs
output_file = outputs/index.porter.stoplist.2docs.out
results_file = $(run_tag)

executable = src/question_answering.sh
arguments = $(question_file) $(doc_index) $(run_tag) $(output_file) $(results_file)
Universe = vanilla
getenv = true
output = run_QuAILS.$(run_tag).out
log = run_QuAILS.$(run_tag).log
error = run_QuAILS.$(run_tag).err
transfer_executable = false
request_memory = 1024
#Queue

doc_index = /home2/cjaja/classwork/spring-2014/ling573/question-answering/src/indexes/index.krovetz.stoplist
run_tag = index.krovetz.stoplist.2docIDs
output_file = outputs/index.krovetz.stoplist.2docIDs.out
results_file = $(run_tag)
Queue

doc_index = /home2/cjaja/classwork/spring-2014/ling573/question-answering/src/indexes/index.none.stoplist
run_tag = index.none.stoplist.2docIDs
output_file = outputs/index.none.stoplist.2docIDs.out
results_file = $(run_tag)
#Queue

doc_index = /home2/cjaja/classwork/spring-2014/ling573/question-answering/src/indexes/index.none.none
run_tag = index.none.none
output_file = outputs/index.none.none.2docIDs.out
results_file = $(run_tag)
#Queue
