question_file = /dropbox/13-14/573/Data/Questions/devtest/TREC-2006.xml
doc_index = /home2/cjaja/classwork/spring-2014/ling573/question-answering/src/indexes/index.porter.stoplist
web_cache = src/cached_web_results/TREC-2006.3pg.web_cache
run_tag = 15
output_file = outputs/$(run_tag).out
results_file = $(run_tag)

executable = src/question_answering.sh
arguments = $(question_file) $(doc_index) $(web_cache) $(run_tag) $(output_file) $(results_file)
Universe = vanilla
getenv = true
output = run_QuAILS.$(run_tag).out
log = run_QuAILS.$(run_tag).log
error = run_QuAILS.$(run_tag).err
transfer_executable = false
request_memory = 1024
Queue

web_cache = src/cached_web_results/TREC-2006.5pg.web_cache
run_tag = 16
Queue

web_cache = src/cached_web_results/TREC-2006.6pg.web_cache
run_tag = 17
Queue
