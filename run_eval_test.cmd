run_tag = eval_test
q_file = /dropbox/13-14/573/Data/Questions/evaltest/QA2007_testset.xml
web_cache = src/cached_web_results/QA2007_testset.3pg.web_cache
index = src/indexes/AQUAINT-2/porter.stoplist

executable = src/question_answering_evaltest.sh
arguments = $(run_tag) q_file=$(q_file) web_cache=$(web_cache) index=$(index)
Universe = vanilla
getenv = true
output = $(run_tag).out
log = $(run_tag).log
error = $(run_tag).err
transfer_executable = false
request_memory = 1024
Queue

