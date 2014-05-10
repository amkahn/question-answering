# Claire Jaja
# 5/10/2014
# LING 573 Question Answering
# cache web results

q_file = /dropbox/13-14/573/Data/Questions/devtest/TREC-2006.xml
out_file = cached_web_results/TREC-2006.web_cache

Executable = cached_web_results/cache_web_results.py
Output = cached_web_results/cache_web_results.$(q_file).out
Error = cached_web_results/cache_web_results.$(q_file).err
Log = cached_web_results/cache_web_results.$(q_file).log
Arguments = "$(q_file) $(out_file)"
transfer_executable = false
Queue
