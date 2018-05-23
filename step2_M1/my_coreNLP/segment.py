#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module my_coreNLP/segment
# Author : SABLAYROLLES Louis
# Date : 09 / 05 / 17

# own class of segment parse of corenlp

import my_coreNLP.parseNLP as parseNLP

from test.data_long_sentences import tab

class Spliter:
	def __init__(self, list_punct_simple = [';','(',')'], list_punct_cmplx = ["--"]):
		self.list_punct_simple = list_punct_simple
		self.list_punct_cmplx = list_punct_cmplx
	
	def getListPunctSimple(self):
		return self.list_punct_simple
		
	def getListPunctCmplx(self):
		return self.list_punct_cmplx
		
	def setListPunctSimple(self, list):
		self.list_punct_simple = list
	
	def setListPunctCmplx(self, list):
		self.list_punct_cmplx = list
	
	def punct_split(tab_sentences):
		lEDU = []
		for s in tab_sentences:
			oldc = ""
			l = ""
			for c in s:
				if c in self.list_punct_simple or oldc+c in self.list_punct_cmplx:
					lEDU.append(l)
					l = ""
				l += c
		return lEDU
		

if __name__ == "__main__":
	sNLP = parseNLP.StanfordNLP()
	
	for sentences in tab:
		sentences_tab = sNLP.segmente(sentences) #segmentation par phrase
		
		sSpliter = Spliter()
		EDU_punct_tab = sSpliter.punct_split(sentences_tab)
		
		print(EDU_punct_tab)