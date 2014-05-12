question_file = test.TREC-2006.xml.first_100_lines
doc_index = /home2/cjaja/classwork/spring-2014/ling573/question-answering/src/indexes/index.porter.none
web_cache = src/cached_web_results/TREC-2006.web_cache
run_tag = test
output_file = outputs/test.outputs
results_filename = test

executable = src/question_answering.sh
arguments = $(question_file) $(doc_index) $(web_cache) $(run_tag) $(output_file) $(results_filename)
Universe = vanilla
getenv = true
output = test.out
log = test.log
error = test.err
transfer_executable = false
request_memory = 1024
queue
