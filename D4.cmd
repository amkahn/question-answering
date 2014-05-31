run_tag = 2006
# params
 
executable = src/question_answering.sh
arguments = $(run_tag)
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
# params

executable = src/question_answering_evaltest.sh
arguments = $(run_tag)

Queue
