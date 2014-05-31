run_tag = 2006
indri_passages = 20
passage_length = 75
indri_window_size = 30

executable = src/question_answering.sh
arguments = $(run_tag) indri_passages=$(indri_passages) passage_length=$(passage_length) indri_window_size=$(indri_window_size)
Universe = vanilla
getenv = true
output = $(run_tag).out
log = $(run_tag).log
error = $(run_tag).err
transfer_executable = false
request_memory = 1024*16
Queue

run_tag = 2007
q_file = /dropbox/13-14/573/Data/Questions/evaltest/QA2007_testset.xml
web_cache = src/cached_web_results/QA2007_testset.3pg.web_cache
index = src/indexes/AQUAINT-2/porter.stoplist

executable = src/question_answering_evaltest.sh
arguments = $(run_tag) q_file=$(q_file) web_cache=$(web_cache) index=$(index) indri_passages=$(indri_passages) passage_length=$(passage_length) indri_window_size=$(indri_window_size)

Queue
