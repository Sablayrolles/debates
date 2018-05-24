#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module my_coreNLP/segment
# Author : SABLAYROLLES Louis
# Date : 24 / 05 / 17

# own class of segment parse of corenlp

import pprint

"""
	Module segment
	===============
	
	This module can be use with its own class to segment texts.
	
"""

def VB_Before(min_id, id, tokens):
	"""
		VB_Before(min_id, id, tokens)
		-----------------------------
		
		Test if a verb present before the word id.
		
		:param min_id: id tokens min pour commencer les recherches
		:param id: id du token jusqu'ou rechercher
		:param tokens: liste des tokens de corenlp
		:type min_id: int 
		:type id: int
		:type tokens: list
		:return: True if a verbe is present before the tokens number id
		:rtype: Boolean
	"""
	p = False
	i = min_id
	while not p and i < id:
		p = 'VB' in tokens[i]['pos'] or 'MD' in tokens[i]['pos']
		i += 1
	return p
	
def VB_After(id, tokens):
	"""
		VB_After(id, tokens)
		-----------------------------
		
		Test if a verb present after the word id.
		
		:param id: id du token jusqu'ou rechercher
		:param tokens: liste des tokens de corenlp
		:type id: int
		:type tokens: list
		:return: True if a verbe is present after the tokens number id
		:rtype: Boolean
	"""
	p = False
	i = id + 1
	while not p and i < max(tokens.keys()):
		p = 'VB' in tokens[i]['pos'] or 'MD' in tokens[i]['pos']
		i += 1
	return p

class LinksWords:
	"""
		Class LinksWords
		=================
		
		Use it to manage link_words
		
		def __init__(self) : creating the link_words list
		def list(self) : return the link_words list
		def add(self, word) : add a link word to the list if not present
		def remove(self, word) : delete a link word to the list if present
		def isPresent(self, word) : test if a link word is present in the list
		def default(self) : set the link_words list to a default list of some english link_words.
	"""
	def __init__(self):
		"""
			def __init__(self)
			------------------
			
			creating the link_words list
		"""
		self.link_words = []
	
	def list(self):
		"""
			def list(self)
			--------------
			
			return the link_words list
		"""
		return self.link_words
	
	def add(self, word):
		"""
			def add(self, word)
			-------------------
			
			add a link word to the list if not present
			
			:param word: word to add
			:type word: string
		"""
		if word not in self.link_words:
			self.link_words.append(word)
	
	def remove(self, word):
		"""
			def remove(self, word)
			----------------------
			
			remove a link word to the list if present
			
			:param word: word to delete
			:type word: string
		"""
		if word in self.link_words:
			self.link_words.remove(word)
	
	def isPresent(self, word):
		"""
			def isPresent(self, word)
			-------------------------
			
			test if a link word is present in the list
			
			:param word: word to search
			:type word: string
		"""
		return word in self.link_words

	def default(self):
		"""
			def default(self)
			-----------------
			
			set the link_words list to a default list of some english link_words.
		"""
		self.link_words = ['accordingly', 'actually', 'and', 'also', 'although', 'as', 'because', 'besides', 'but', 'consequently', 'conversely', 'eventually', 'firstly', 'furthermore', 'how', 'hence', 'however', 'if', 'meanwhile', 'moreover', 'namely', 'nevertheless', 'next', 'nonetheless', 'once', 'otherwise', 'secondly', 'similarly', 'since', 'so', 'still', 'that', 'then', 'therefore', 'thirdly', 'though', 'thus', 'till', 'tofirst', 'unless', 'unlike', 'until', 'whatever', 'when', 'whenever', 'where', 'whereas', 'whether', 'while', 'while', 'who', 'yet']

class Spliter:
	"""
		Class Spliter
		=============
		
		Use it to split sentences in EDU
		
		def __init__(self, sNLP, link_words=None, list_punct_simple = [';','(',')'], list_punct_cmplx = ["--"]) : initialize the splitter
		def getListPunctSimple(self) : return the list of punctuation with only one character
		def getListPunctCmplx(self)	: return the list of punctuation with only two character
		def setListPunctSimple(self) : set the list of punctuation with only one character
		def setListPunctCmplx(self) : set the list of punctuation with only two character
		def punct_split(self, sentence) : split a sentence over the punctuation
		def linkwords_split(self, tab_sentences) : split a tabular of sentences or EDU over the linkwords and minor ponctuation (',', ':')
	"""
	def __init__(self, sNLP, link_words=None, list_punct_simple = [';','(',')'], list_punct_cmplx = ["--"]):
		"""
			def __init__(self, sNLP, link_words=None, list_punct_simple = [';','(',')'], list_punct_cmplx = ["--"])
			-------------------------------------------------------------------------------------------------------
			
			initialize the splitter
			
			:param sNLP: StanfordCoreNLP object(parseNLP.py)
			:param link_words: link object
			:param list_punct_simple: list of punctuation with only one character
			:param list_punct_cmplx: list of punctuation with only two character
			:type sNLP: object 
			:type link_words: object
			:type list_punct_simple: string list
			:type list_punct_cmplx: string list
		"""
		if link_words == None:
			self.link_words = LinksWords()
			self.link_words.default()
		self.list_punct_simple = list_punct_simple
		self.list_punct_cmplx = list_punct_cmplx
		self.sNLP = sNLP
	
	def getListPunctSimple(self):
		"""
			def getListPunctSimple(self)
			----------------------------
			
			return the list of punctuation with only one character
			
			:return: list of one character's ponctuation
			:rtype: string list
		"""
		return self.list_punct_simple
		
	def getListPunctCmplx(self):
		"""
			def getListPunctCmplx(self)
			---------------------------
			
			return the list of punctuation with only two character
			
			:return: list of one character's ponctuation
			:rtype: string list
		"""
		return self.list_punct_cmplx
		
	def setListPunctSimple(self, list):
		"""
			def setListPunctSimple(self)
			----------------------------
			
			set the list of punctuation with only one character
			
			:param list: list of one character's ponctuation
			:type list: string list
		"""
		self.list_punct_simple = list
	
	def setListPunctCmplx(self, list):
		"""
			def setListPunctCmplx(self)
			---------------------------
			
			set the list of punctuation with only two character
			
			:param list: list of two character's ponctuation
			:type list: string list
		"""
		self.list_punct_cmplx = list
	
	def punct_split(self, sentence):
		"""
			def punct_split(self, sentence)
			-------------------------------
			
			split a sentence over the punctuation
			
			:param sentence: sentence to split
			:type sentence: string 
			:return: list of EDU
			:rtype: string list
		"""
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
		"""
			def linkwords_split(self, tab_sentences)
			----------------------------------------
			
			split a tabular of sentences or EDU over the linkwords and minor ponctuation (',', ':')
			
			:param tab_sentences: list of sentences or EDU to split
			:type tab_sentences: string list
			:return: list of EDU
			:rtype: string list
		"""
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
