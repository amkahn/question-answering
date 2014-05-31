run_tag = 2006

executable = src/question_answering.sh
arguments = $(run_tag)
Universe = vanilla
getenv = true
output = $(run_tag).out
log = $(run_tag).log
error = $(run_tag).err
transfer_executable = false
request_memory = 18*1024
Queue

