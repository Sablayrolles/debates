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

sys.path.append("../..")
import tools.RappelPrecisionFMesure as RPF

from data_sentences import tab

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
	
	rpf_sentences = RPF.FScores(tab.keys())
	rpf_punct = RPF.FScores(tab.keys())
	
	for kind in tab.keys():
		for sentences, want in zip(tab[kind], tab_segmented[kind]):
			print("Sentences :")
			print(sentences)
			sentences_tab = sNLP.segmente(sentences) #segmentation par phrase
			print("\nSentence splitter : ")
			print_tab(sentences_tab)
			print("\nReal :")
			print_tab(want)
			
			rpf_sentences.saisieScore(kind)

			sSpliter = Spliter(sNLP)
			EDU_punct_tab = []
			for s in sentences_tab:
				EDU_punct_tab.extend(sSpliter.punct_split(s))
			
			print("\nReal :")
			print_tab(want)
			
			print("\nPunct splitter : ")
			print_tab(EDU_punct_tab)
			print("\n#################################")

			rpf_punct.saisieScore(kind)

			#EDUs = sSpliter.linkwords_split(EDU_punct_tab)
			#print("\nlink_words splitter : ")
			#print_tab(EDUs)
			#print("\n\n----------------------------------------------------------------------------------------------------\n\n")
		
	for kind in tab.keys():
		print("**** Kind", kind, "****")
		print("- Sentences")
		print("\tP:", rpf_sentences.getMoyPrecision(kind))
		print("\tR:", rpf_sentences.getMoyRappel(kind))
		print("\tFMesures:", rpf_sentences.getMoyFMesure(kind))
		print("- Punct")
		print("\tP:", rpf_punct.getMoyPrecision(kind))
		print("\tR:", rpf_punct.getMoyRappel(kind))
		print("\tFMesures:", rpf_punct.getMoyFMesure(kind))
