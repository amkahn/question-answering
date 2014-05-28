# Claire Jaja
# 5/10/2014
# LING 573 Question Answering
# cache web results

num_pages = 5
q_file = /dropbox/13-14/573/Data/Questions/devtest/TREC-2006.xml
q_name = TREC-2006.$(num_pages)pg

Executable = cache_web_results.py
Output = cached_web_results/cache_web_results.$(q_name).out
Error = cached_web_results/cache_web_results.$(q_name).err
Log = cached_web_results/cache_web_results.$(q_name).log
Arguments = "$(q_file) cached_web_results/$(q_name).web_cache $(num_pages)"
transfer_executable = false
Queue
