run_tag = 21b
num_lin_exp_terms = 5
weight_lin_exp_query = 0.2
passages_per_answer_candidate = 2

executable = src/question_answering.sh
arguments = $(run_tag) num_lin_exp_terms=$(num_lin_exp_terms) weight_lin_exp_query=$(weight_lin_exp_query) passages_per_answer_candidate=$(passages_per_answer_candidate)
Universe = vanilla
getenv = true
output = $(run_tag).out
log = $(run_tag).log
error = $(run_tag).err
transfer_executable = false
request_memory = 1024*18
Queue

run_tag = 22b
num_lin_exp_terms = 5
weight_lin_exp_query = 0.2
passages_per_doc_id = 2
passages_per_answer_candidate = 2
arguments = $(run_tag) num_lin_exp_terms=$(num_lin_exp_terms) weight_lin_exp_query=$(weight_lin_exp_query) passages_per_doc_id=$(passages_per_doc_id) passages_per_answer_candidate=$(passages_per_answer_candidate)
Queue

run_tag = 23b
num_lin_exp_terms = 10
weight_lin_exp_query = 0.2
passages_per_doc_id = 2
arguments = $(run_tag) num_lin_exp_terms=$(num_lin_exp_terms) weight_lin_exp_query=$(weight_lin_exp_query) passages_per_doc_id=$(passages_per_doc_id)
Queue

run_tag = 24b
num_lin_exp_terms = 10
weight_lin_exp_query = 0.2
passages_per_answer_candidate = 2
arguments = $(run_tag) num_lin_exp_terms=$(num_lin_exp_terms) weight_lin_exp_query=$(weight_lin_exp_query) passages_per_answer_candidate=$(passages_per_answer_candidate)
Queue

run_tag = 25b
num_lin_exp_terms = 10
weight_lin_exp_query = 0.2
passages_per_doc_id = 2
passages_per_answer_candidate = 2
arguments = $(run_tag) num_lin_exp_terms=$(num_lin_exp_terms) weight_lin_exp_query=$(weight_lin_exp_query) passages_per_doc_id=$(passages_per_doc_id) passages_per_answer_candidate=$(passages_per_answer_candidate)
Queue

run_tag = 26b
num_web_exp_terms = 10
num_lin_exp_terms = 10
weight_lin_exp_query = 0.2
passages_per_doc_id = 2
arguments = $(run_tag) num_web_exp_terms=$(num_web_exp_terms) num_lin_exp_terms=$(num_lin_exp_terms) weight_lin_exp_query=$(weight_lin_exp_query) passages_per_doc_id=$(passages_per_doc_id)
Queue

run_tag = 27b
num_web_exp_terms = 10
num_lin_exp_terms = 10
weight_lin_exp_query = 0.2
passages_per_answer_candidate = 2
arguments = $(run_tag) num_web_exp_terms=$(num_web_exp_terms) num_lin_exp_terms=$(num_lin_exp_terms) weight_lin_exp_query=$(weight_lin_exp_query) passages_per_answer_candidate=$(passages_per_answer_candidate)
Queue

run_tag = 28b
ne_upweighting = 1.5
num_web_exp_terms = 10
num_lin_exp_terms = 10
weight_lin_exp_query = 0.2
passages_per_doc_id = 2
passages_per_answer_candidate = 2
arguments = $(run_tag) ne_upweighting=$(ne_upweighting) num_web_exp_terms=$(num_web_exp_terms) num_lin_exp_terms=$(num_lin_exp_terms) weight_lin_exp_query=$(weight_lin_exp_query) passages_per_doc_id=$(passages_per_doc_id) passages_per_answer_candidate=$(passages_per_answer_candidate)
Queue

run_tag = 29b
ne_upweighting = 1.5
num_web_exp_terms = 10
num_lin_exp_terms = 10
weight_lin_exp_query = 0.2
passages_per_doc_id = 2
arguments = $(run_tag) ne_upweighting=$(ne_upweighting) num_web_exp_terms=$(num_web_exp_terms) num_lin_exp_terms=$(num_lin_exp_terms) weight_lin_exp_query=$(weight_lin_exp_query) passages_per_doc_id=$(passages_per_doc_id)
Queue

run_tag = 30b
ne_upweighting = 1.5
num_web_exp_terms = 10
num_lin_exp_terms = 10
weight_lin_exp_query = 0.2
passages_per_answer_candidate = 2
arguments = $(run_tag) ne_upweighting=$(ne_upweighting) num_web_exp_terms=$(num_web_exp_terms) num_lin_exp_terms=$(num_lin_exp_terms) weight_lin_exp_query=$(weight_lin_exp_query) passages_per_answer_candidate=$(passages_per_answer_candidate)
Queue



