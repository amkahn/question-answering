#!/opt/python-2.7/bin/python2.7
#
# script can be run without invoking python because of shebang
# will be run with correct version on Patas
#
# LING 573 Question Answering System
# Code last updated on 6/4/2014 by Claire Jaja
#
# This script will do error analysis on the output of the compute_MRR script

import sys

def main():
	# first argument is the results file
    results_file = open(sys.argv[1],'r')

    total_answer = 0
    correct_answer = 0
    top_10 = 0
    first_answer = 0

    for line in results_file:	
        line = line.split(":")
        if len(line) == 2:
            question = line[0]
            result = line[1]
            # ignore no factoid pattern ones
            if len(question.split()) == 1 and question.strip() != "Aggregate":
                total_answer += 1
                result = float(result)
                if result != 0.0:
                    correct_answer += 1
                if result >= 0.1:
                    top_10 += 1
                if result == 1.0:
                    first_answer += 1

    print("Out of %s questions answered, %s had the correct answer at all, %s had the correct answer in the top 10, and %s had the correct answer as the first answer." % (total_answer,correct_answer,top_10,first_answer))


if __name__ == '__main__':
	main()
