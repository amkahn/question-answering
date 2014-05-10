# Claire Jaja
# 5/10/2014
# LING 573 Question Answering
# cache web results

q_name = TREC-2006
q_file = /dropbox/13-14/573/Data/Questions/devtest/TREC-2006.xml

Executable = cached_web_results/cache_web_results.py
Output = cached_web_results/cache_web_results.$(q_name).out
Error = cached_web_results/cache_web_results.$(q_name).err
Log = cached_web_results/cache_web_results.$(q_name).log
Arguments = "$(q_file) cached_web_results/$(q_name).web_cache"
transfer_executable = false
Queue
