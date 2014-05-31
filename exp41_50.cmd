run_tag = 41
target_upweighting = 2

executable = src/question_answering.sh
arguments = $(run_tag) target_upweighting=$(target_upweighting)
Universe = vanilla
getenv = true
output = $(run_tag).out
log = $(run_tag).log
error = $(run_tag).err
transfer_executable = false
request_memory = 1024*15
Queue

run_tag = 42
indri_passages = 20

arguments = $(run_tag) indri_passages=$(indri_passages)

Queue

run_tag = 43
indri_passages=60

Queue

run_tag = 44
indri_passages=80

Queue

run_tag = 45
num_docs = 2

arguments = $(run_tag) num_docs=$(num_docs)

Queue

run_tag = 46
num_passages = 5
snippet_passage_count = 5

arguments = $(run_tag) num_passages=$(num_passages) snippet_passage_count=$(snippet_passage_count)

Queue

run_tag = 47

num_passages = 3
snippet_passage_count = 3

Queue

run_tag = 48

num_passages = 1
snippet_passage_count = 1

Queue

run_tag = 49
indri_passages = 20
passage_length = 75
indri_window_size = 30

arguments = $(run_tag) indri_passages=$(indri_passages) passage_length=$(passage_length) indri_window_size=$(indri_window_size)

Queue

run_tag = 50

indri_passages = 60

Queue
