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
