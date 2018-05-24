#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module my_coreNLP/segment
# Author : SABLAYROLLES Louis
# Date : 09 / 05 / 17

# own class of segment parse of corenlp

import parseNLP as parseNLP
import pprint

from test.data_long_sentences import tab

def VB_Before(min_id, id, tokens):
	p = False
	i = min_id
	while not p and i < id:
		p = 'VB' in tokens[i]['pos'] or 'MD' in tokens[i]['pos']
		i += 1
	return p
	
def VB_After(id, tokens):
	p = False
	i = id + 1
	while not p and i < max(tokens.keys()):
		p = 'VB' in tokens[i]['pos'] or 'MD' in tokens[i]['pos']
		i += 1
	return p

class LinksWords:
	def __init__(self):
		self.link_words = []
	
	def list(self):
		return self.link_words
	
	def add(self, word):
		if word not in self.link_words:
			self.link_words.append(word)
	
	def remove(self, word):
		if word in self.link_words:
			self.link_words.remove(word)
	
	def isPresent(self, word):
		return word in self.link_words

	def default(self):
		self.link_words = ['accordingly', 'actually', 'and', 'also', 'although', 'as', 'because', 'besides', 'but', 'consequently', 'conversely', 'eventually', 'firstly', 'furthermore', 'how', 'hence', 'however', 'meanwhile', 'moreover', 'namely', 'nevertheless', 'next', 'nonetheless', 'once', 'otherwise', 'secondly', 'similarly', 'since', 'so', 'still', 'that', 'then', 'therefore', 'thirdly', 'though', 'thus', 'till', 'tofirst', 'unless', 'unlike', 'until', 'whatever', 'when', 'whenever', 'where', 'whereas', 'whether', 'while', 'while', 'yet']

class Spliter:
	def __init__(self, sNLP, link_words=None, list_punct_simple = [';','(',')'], list_punct_cmplx = ["--"]):
		self.link_words = LinksWords()
		self.link_words.default()
		self.list_punct_simple = list_punct_simple
		self.list_punct_cmplx = list_punct_cmplx
		self.sNLP = sNLP
	
	def getListPunctSimple(self):
		return self.list_punct_simple
		
	def getListPunctCmplx(self):
		return self.list_punct_cmplx
		
	def setListPunctSimple(self, list):
		self.list_punct_simple = list
	
	def setListPunctCmplx(self, list):
		self.list_punct_cmplx = list
	
	def punct_split(self, sentence):
		lEDU = []
		oldc = ""
		l = ""
		for c in sentence:
			l += c
			if c in self.list_punct_simple or oldc+c in self.list_punct_cmplx:
				if oldc == c and c == "-":
					lEDU.append(l[:-2])
					l = "--"
				else:
					lEDU.append(l)
					l = ""
			oldc = c
		lEDU.append(l)
		
		return lEDU
	
	def linkwords_split(self, tab_sentences):
		lEDU = []
		
		for s in tab_sentences:
			dependancy = self.sNLP.dependency_parse(s)
			tokens = self.sNLP.getTokens(s)
			l = ""
			min_id = 1
			for id in tokens.keys():
				if tokens[id]['lemma'] in self.link_words.list():
					if VB_Before(min_id, id, tokens) and VB_After(id, tokens):
						#on split
						lEDU.append(l)
						l = ""
						min_id = id
				l += " " + tokens[id]['word']
			lEDU.append(l)
		
		lEDU2 = []
		for s in lEDU:
			dependancy = self.sNLP.dependency_parse(s)
			tokens = self.sNLP.getTokens(s)
			l = ""
			min_id = 1
			for id in tokens.keys():
				l += " " + tokens[id]['word']
				if tokens[id]['lemma'] in [',', ":"]:
					if VB_Before(min_id, id, tokens) and VB_After(id, tokens):
						#on split
						lEDU2.append(l)
						l = ""
						min_id = id
			lEDU2.append(l)
		return lEDU2

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
