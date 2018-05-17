#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module my_coreNLP/test_parse_sentences
# Author : SABLAYROLLES Louis
# Date : 17 / 05 / 17

# file to test parse of corenlp on sentences

import parseNLP
from test.data_long_sentences import tab


sNLP = parseNLP.StanfordNLP()
for s in tab:
	print("In:", s)
	t = sNLP.segmente(s)
	print(t)