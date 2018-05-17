#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module my_coreNLP/test_parse_segmentation.py
# Author : SABLAYROLLES Louis
# Date : 17 / 05 / 17

# test decoupage sur segment

import pprint
import segment
import parseNLP
from test.data_long_sentences import tab

sNLP = parseNLP.StanfordNLP()
for bloc in tab:
	print("In:", bloc)
	print("\t[NLP] Splitting in sentence")
	sentences = sNLP.segmente(bloc)
	print("\t[NLP] End splitting",len(sentences),"sentences obtained")
	print("\n\n")

	for s in sentences:
		print("\t\t[Segment] Analysing ",s)
		myP = segment.Parser(s)
		print("\t\t[Segment] Cutting sentence in EDU")
		seg = myP.segmente()
		print("\t\t[Segment] End cutting", len(seg), "EDU obtained")
		pprint.pprint(seg)
		print("\n\n")
