question_file = /dropbox/13-14/573/Data/Questions/devtest/TREC-2006.xml
doc_index = /home2/cjaja/classwork/spring-2014/ling573/question-answering/src/indexes/index.porter.stoplist
web_cache = src/cached_web_results/TREC-2006.3pg.web_cache
run_tag = return_passage_centered
output_file = outputs/$(run_tag).outputs
results_file = $(run_tag)

executable = src/question_answering.sh
arguments = $(question_file) $(doc_index) $(web_cache) $(run_tag) $(output_file) $(results_file)
Universe = vanilla
getenv = true
output = $(run_tag).out
log = $(run_tag).log
error = $(run_tag).err
transfer_executable = false
request_memory = 1024
Queue

