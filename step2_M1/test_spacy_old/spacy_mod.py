#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module spacy_mod
# Author : SABLAYROLLES Louis
# Date : 07 / 05 / 17

import spacy

"""
	Module spacy_mod
	================
	
	This module can be use with its own class to interact with stanfordcorenlp java api.
	
"""

class Spacy:
	"""
		Class Spacy
		===========
		
		Use it to define a spacy of object to interact with.
		
		def __init__(self) : instanciation of spacy object
		def analyse(self, text) : do the analysis with spacy
		def getEntities(self) : return spacy entities of sentence analyse
		def tokens(self) : return spacy tokens of sentence analyse
		def outputDependancy(self) : plot the dependancies in the sentence
		def getSentiment(self) : return spacy sentiment on sentence anlyse
		
	"""
	
	def __init__(self):
		"""
			def __init__(self)
			------------------
			
			instanciation of timer object
			
			:return: None
			:rtype: NoneType
		"""
		self.nlp = spacy.load('en_core_web_sm')
		self.doc = {}
	
	def analyse(self, text):
		"""
			def analyse(self, text)
			-----------------------
			
			do the analysis with spacy
			
			:param text: text to analyse
			:type text: string
			:return: None
			:rtype: NoneType
		"""
			
		self.doc = self.nlp(text)
	
	def getEntities(self):
		"""
			def getEntities(self)
			---------------------
			
			return spacy entities of sentence analyse

			:return: spacy entities
			:rtype: dictionnary
		"""
		if self.doc != {}:
			t = {}
			for entity in self.doc.ents:
				t[entity.text] = entity.label_
				
			return t
		else:
			return {}

	def tokens(self):
		"""
			def tokens(self)
			----------------
			
			return spacy tokens of sentence analyse

			:return: spacy tokens
			:rtype: dictionnary
		"""
		if self.doc != {}:
			t = {}
			for token in self.doc:
				t[token.text] = token
			return t
		else:
			return {}
		
	def outputDependancy(self):
		"""
			def outputDependancy(self)
			--------------------------
			
			plot the dependancies in the sentence

			:return: spacy entities
			:rtype: dictionnary
		"""
		print("graph (open with localhost:port on a navigator")
		spacy.displacy.serve(self.doc,style="dep")
		
	def getSentiment(self):
		"""
			def getSentiment(self)
			----------------------
			
			return spacy sentiment on sentence anlyse

			:return: spacy sentiment
			:rtype: int
		"""
		return self.doc.sentiment
