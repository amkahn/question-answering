run_tag = test_eval_test
q_file = /dropbox/13-14/573/Data/Questions/evaltest/QA2007_testset.xml
web_cache = src/cached_web_results/QA2007_testset.3pg.web_cache
index = src/indexes/AQUAINT-2/porter.stoplist
passages_per_doc_id = 2
passages_per_answer_candidate = 4


executable = src/question_answering_evaltest.sh
arguments = $(run_tag) q_file=$(q_file) web_cache=$(web_cache) index=$(index) passages_per_doc_id=$(passages_per_doc_id) passages_per_answer_candidate=$(passages_per_answer_candidate)
Universe = vanilla
getenv = true
output = $(run_tag).out
log = $(run_tag).log
error = $(run_tag).err
transfer_executable = false
request_memory = 1024
Queue

