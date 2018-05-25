#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module my_coreNLP/test/test_segment
# Author : SABLAYROLLES Louis
# Date : 24 / 05 / 17

# run test over the segment module

import sys
sys.path.append("..")
import parseNLP
import segment

from test.data_sentences import tab

"""
	Module Test-Segment
	===================
	
	This module can be use to do module segment on the module parseNLP
	
"""

def print_tab(t):
	i = 0
	for e in t:
		print("["+str(i)+"]",e)
		i += 1


if __name__ == "__main__":
	sNLP = parseNLP.StanfordNLP()
	
	for sentences in tab:
		print("Sentences :")
		print(sentences)
		sentences_tab = sNLP.segmente(sentences) #segmentation par phrase
		print("\nSentence splitter : ")
		print_tab(sentences_tab)
		

		sSpliter = Spliter(sNLP)
		EDU_punct_tab = []
		for s in sentences_tab:
			EDU_punct_tab.extend(sSpliter.punct_split(s))
			
		print("\nPunct splitter : ")
		print_tab(EDU_punct_tab)
		print("\n#################################")


		EDUs = sSpliter.linkwords_split(EDU_punct_tab)
		print("\nlink_words splitter : ")
		print_tab(EDUs)
		print("\n\n----------------------------------------------------------------------------------------------------\n\n")