run_tag = 1
passage_length = 75
window_size = 30

executable = src/question_answering.sh
arguments = $(run_tag) passage_length=$(passage_length) window_size=$(window_size)
Universe = vanilla
getenv = true
output = $(run_tag).out
log = $(run_tag).log
error = $(run_tag).err
transfer_executable = false
request_memory = 1024
Queue

run_tag = 2
passage_length = 150
window_size = 75

Queue

run_tag = 3
snippet_weight = 0.99

arguments = $(run_tag) snippet_weight=$(snippet_weight)

Queue

run_tag = 4
snippet_weight = 0.8

arguments = $(run_tag) snippet_weight=$(snippet_weight)

Queue

run_tag = 5
web_cache = src/cached_web_results/TREC-2006.2pg.web_cache

arguments = $(run_tag) web_cache=$(web_cache)

Queue

run_tag = 6
web_cache = src/cached_web_results/TREC-2006.4pg.web_cache

arguments = $(run_tag) web_cache=$(web_cache)

Queue

run_tag = 7
web_cache = src/cached_web_results/TREC-2006.2pg.web_cache
snippet_weight = 0.99

arguments = $(run_tag) web_cache=$(web_cache) snippet_weight=$(snippet_weight)

Queue

run_tag = 8
web_cache = src/cached_web_results/TREC-2006.4pg.web_cache
snippet_weight = 0.99

arguments = $(run_tag) web_cache=$(web_cache) snippet_weight=$(snippet_weight)

Queue

run_tag = 9
web_cache = src/cached_web_results/TREC-2006.2pg.web_cache
snippet_weight = 0.8

arguments = $(run_tag) web_cache=$(web_cache) snippet_weight=$(snippet_weight)

Queue

run_tag = 10
web_cache = src/cached_web_results/TREC-2006.4pg.web_cache
snippet_weight = 0.8

arguments = $(run_tag) web_cache=$(web_cache) snippet_weight=$(snippet_weight)

Queue



