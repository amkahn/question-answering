run_tag = 51
indri_passages = 20
passage_length = 50
indri_window_size = 25

executable = src/question_answering.sh
arguments = $(run_tag) indri_passages=$(indri_passages) passage_length=$(passage_length) indri_window_size=$(indri_window_size)
Universe = vanilla
getenv = true
output = $(run_tag).out
log = $(run_tag).log
error = $(run_tag).err
transfer_executable = false
request_memory = 1024*15
Queue

run_tag = 52

web_cache = src/cached_web_results/TREC-2006.4pg.web_cache

arguments = $(run_tag) indri_passages=$(indri_passages) passage_length=$(passage_length) indri_window_size=$(indri_window_size) web_cache=$(web_cache)

Queue

run_tag = 53

passage_length = 75
indri_window_size = 30
passages_per_answer_candidate = 2

arguments = $(run_tag) indri_passages=$(indri_passages) passage_length=$(passage_length) indri_window_size=$(indri_window_size) passages_per_answer_candidate=$(passages_per_answer_candidate)

Queue

run_tag = 54
snippet_weight = 0.99

arguments = $(run_tag) indri_passages=$(indri_passages) passage_length=$(passage_length) indri_window_size=$(indri_window_size) passages_per_answer_candidate=$(passages_per_answer_candidate) snippet_weight=$(snippet_weight)

Queue

run_tag = 55

arguments = $(run_tag) indri_passages=$(indri_passages) passage_length=$(passage_length) indri_window_size=$(indri_window_size) passages_per_answer_candidate=$(passages_per_answer_candidate) snippet_weight=$(snippet_weight) web_cache=$(web_cache)

Queue
