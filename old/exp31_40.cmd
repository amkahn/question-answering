run_tag = 31
ne_upweighting  = 1.5
num_web_exp_terms = 10
num_lin_exp_terms = 10
weight_lin_exp_query =0.2
passages_per_doc_id = 2
passages_per_answer_candidate = 2

executable = src/question_answering.sh
arguments = $(run_tag) ne_upweighting=$(ne_upweighting) num_web_exp_terms=$(num_web_exp_terms) num_lin_exp_terms=$(num_lin_exp_terms) weight_lin_exp_query=$(weight_lin_exp_query) passages_per_doc_id=$(passages_per_doc_id) passages_per_answer_candidiate=$(passages_per_answer_candidate)
Universe = vanilla
getenv = true
output = $(run_tag).out
log = $(run_tag).log
error = $(run_tag).err
transfer_executable = false
request_memory = 1024*15
Queue

run_tag = 32
web_cache = src/cached_web_results/TREC-2006.4pg.web_cache 
num_web_exp_terms = 10
passage_length = 75
snippet_weight = 0.99
indri_window_size = 30
passages_per_answer_candidate = 2

arguments = $(run_tag) web_cache=$(web_cache) num_web_exp_terms=$(num_web_exp_terms) passage_length=$(passage_length) snippet_weight=$(snippet_weight) indri_window_size=$(indri_window_size) passages_per_answer_candidate=$(passages_per_answer_candidate)

Queue

run_tag = 33
web_cache = src/cached_web_results/TREC-2006.5pg.web_cache 


Queue

run_tag = 34
web_cache = src/cached_web_results/TREC-2006.6pg.web_cache 

Queue

run_tag = 35
passages_per_answer_candidate = 2

arguments = $(run_tag) passages_per_answer_candidate=$(passages_per_answer_candidate)

Queue

run_tag = 36

passages_per_answer_candidate = 4

Queue

run_tag = 37
passages_per_doc_id = 2
passages_per_answer_candidate = 4

arguments = $(run_tag) passages_per_doc_id=$(passages_per_doc_id) passages_per_answer_candidate=$(passages_per_answer_candidate)

Queue

run_tag = 38
passages_per_answer_candidate = 6

arguments = $(run_tag) passages_per_answer_candidate=$(passages_per_answer_candidate)

Queue

run_tag = 39
passages_per_doc_id = 4

arguments = $(run_tag) passages_per_doc_id=$(passages_per_doc_id)

Queue

run_tag = 40
passages_per_doc_id = 4
passages_per_answer_candidate = 6

arguments = $(run_tag) passages_per_doc_id=$(passages_per_doc_id) passages_per_answer_candidate=$(passages_per_answer_candidate)

Queue



