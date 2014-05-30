run_tag = 11
passages_per_doc_id = 2

executable = src/question_answering.sh
arguments = $(run_tag) passages_per_doc_id=$(passages_per_doc_id)
Universe = vanilla
getenv = true
output = $(run_tag).out
log = $(run_tag).log
error = $(run_tag).err
transfer_executable = false
request_memory = 1024*15
#Queue

run_tag = 12
passages_per_answer_candidate = 2

arguments = $(run_tag) passages_per_answer_candidate=$(passages_per_answer_candidate)

Queue

run_tag = 13

arguments = $(run_tag) passages_per_doc_id=$(passages_per_doc_id) passages_per_answer_candidate=$(passages_per_answer_candidate)

#Queue

run_tag = 14
ne_upweighting = 1.5

arguments = $(run_tag) passages_per_doc_id=$(passages_per_doc_id) ne_upweighting=$(ne_upweighting)

#Queue

run_tag = 15

arguments = $(run_tag) passages_per_answer_candidate=$(passages_per_answer_candidate) ne_upweighting=$(ne_upweighting)

Queue

run_tag = 16

arguments = $(run_tag) passages_per_doc_id=$(passages_per_doc_id) passages_per_answer_candidate=$(passages_per_answer_candidate) ne_upweighting=$(ne_upweighting)

#Queue

run_tag = 17

num_web_exp_terms = 10

arguments = $(run_tag) passages_per_doc_id=$(passages_per_doc_id) num_web_exp_terms=$(num_web_exp_terms)

Queue

run_tag = 18

arguments = $(run_tag) passages_per_answer_candidate=$(passages_per_answer_candidate) num_web_exp_terms=$(num_web_exp_terms)

#Queue

run_tag = 19

arguments = $(run_tag) passages_per_doc_id=$(passages_per_doc_id) passages_per_answer_candidate=$(passages_per_answer_candidate) num_web_exp_terms=$(num_web_exp_terms)

Queue

run_tag = 20

num_lin_exp_terms = 5
weight_lin_exp_query = 0.2

arguments = $(run_tag) passages_per_doc_id=$(passages_per_doc_id) num_lin_exp_terms=$(num_lin_exp_terms) weight_lin_exp_query=$(weight_lin_exp_query)

#Queue
