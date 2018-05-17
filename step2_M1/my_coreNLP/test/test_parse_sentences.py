#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module my_coreNLP/test_parse_sentences
# Author : SABLAYROLLES Louis
# Date : 17 / 05 / 17

# file to test parse of corenlp on sentences

import sys
sys.path.append("..")

import parseNLP
import pprint
from test.data_long_sentences import tab


sNLP = parseNLP.StanfordNLP()
nb_correct_ended = 0
nb_tt = 0
for s in tab:
	print("In:", s)
	t = sNLP.segmente(s)

	for u in t:
		nb_tt += 1
		if u[-1] in ['.', '!', '?']:
			nb_correct_ended += 1
		print("\t",u)
	print("\n\n")

print("Ratio correct : ", nb_correct_ended, "/", nb_tt);
print("/ : ", float(nb_correct_ended)/float(nb_tt), "% : ", float(nb_correct_ended)/float(nb_tt)*float(100))

