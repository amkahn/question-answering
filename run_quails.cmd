run_tag = param_test
web_cache = src/cached_web_results/TREC-2006.4pg.web_cache

executable = src/question_answering.sh
arguments = $(run_tag) web_cache=$(web_cache)
Universe = vanilla
getenv = true
output = $(run_tag).out
log = $(run_tag).log
error = $(run_tag).err
transfer_executable = false
request_memory = 1024
Queue

