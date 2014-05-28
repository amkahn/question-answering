run_tag = param_test
output_file = outputs/$(run_tag).outputs
results_file = $(run_tag)



executable = src/question_answering_param.sh
arguments =  $(output_file) $(results_file) output_file=$(output_file) run_tag=$(run_tag)
Universe = vanilla
getenv = true
output = $(run_tag).out
log = $(run_tag).log
error = $(run_tag).err
transfer_executable = false
request_memory = 1024
Queue

