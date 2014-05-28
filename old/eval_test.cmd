question_file = /dropbox/13-14/573/Data/Questions/evaltest/QA2007_testset.xml
doc_index = /home2/cjaja/classwork/spring-2014/ling573/question-answering/src/indexes/AQUAINT-2/porter.stoplist
web_cache = src/cached_web_results/QA2007_testset.3pg.web_cache
run_tag = test_evalset
output_file = outputs/$(run_tag).outputs

executable = src/question_answering.py
arguments = $(question_file) $(doc_index) $(web_cache) $(run_tag) $(output_file)
Universe = vanilla
getenv = true
output = $(run_tag).out
log = $(run_tag).log
error = $(run_tag).err
transfer_executable = false
request_memory = 1024
Queue
