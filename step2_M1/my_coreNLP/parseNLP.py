#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module my_coreNLP/parseNLP
# Author : SABLAYROLLES Louis
# Date : 24 / 05 / 17

# own class to interact with stanfordcorenlp java api

from stanfordcorenlp import StanfordCoreNLP
import logging
import json
import pickle
import pprint

"""
	Module parseNLP
	===============
	
	This module can be use with its own class to interact with stanfordcorenlp java api.
	
"""

class StanfordNLP:
	"""
		Class StanfordNLP
		=================
		
		Use it to create a StanfordNLP object to use a stanfordcorenlp lib.
		
		def __init__(self, host='http://localhost', port=9000) : instanciation of StanfordNLP object
		def word_tokenize(self, sentence) : retourne l'objet complet de l'analyse de corenlp
		def pos(self, sentence) : retourne part of speech de l'analyse de corenlp
		def ner(self, sentence) : retourne named entity reference de l'analyse de corenlp
		def parse(self, sentence) :  retourne parse de l'analyse de corenlp
		def dependency_parse(self, sentence) : retourne les dependances de l'analyse de corenlp
		def annotate(self, sentence) : retourne les annotations de l'analyse de corenlp
		def getTokens(self, sentence) : retourne la liste des tokens de l'analyse de corenlp
		def segmente(self, sentence) : retourne la liste des segments de l'analyse de corenlp
	"""
	def __init__(self, host='http://localhost', port=9221):
		"""
			def __init__(self, host='http://localhost', port=9221)
			------------------------------------------------------
			
			instanciation of StanfordNLP object
			
			:param host: adresse où le serveur java de stanford corelnp tourne
			:param port: port sur lequel interroger le serveur java de standford corenlp
			:type host: string 
			:type port: int
		"""
		self.nlp = StanfordCoreNLP(host, port=port,
								   timeout=30000)  # , quiet=False, logging_level=logging.DEBUG)
		self.props = {
			'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,depparse,dcoref,relation',
			'pipelineLanguage': 'en',
			'outputFormat': 'json'
		}

	def word_tokenize(self, sentence):
		"""
			def word_tokenize(self, sentence)
			---------------------------------
			
			retourne l'objet complet de l'analyse de corenlp
			
			:param sentence: phrase a traiter
			:type sentence: string
			:return: analyse de corenlp
			:rtype: json
		"""
		return self.nlp.word_tokenize(sentence)

	def pos(self, sentence):
		"""
			def pos(self, sentence)
			-----------------------
			
			retourne part of speech de l'analyse de corenlp
			
			:param sentence: phrase a traiter
			:type sentence: string
			:return: part of speech de sentence
			:rtype: json
		"""
		return self.nlp.pos_tag(sentence)

	def ner(self, sentence):
		"""
			def ner(self, sentence)
			-----------------------
			
			retourne named entity reference de l'analyse de corenlp
			
			:param sentence: phrase a traiter
			:type sentence: string
			:return: named entity reference de sentence
			:rtype: json
		"""
		return self.nlp.ner(sentence)

	def parse(self, sentence):
		"""
			def parse(self, sentence)
			-------------------------
			
			retourne parse de l'analyse de corenlp
			
			:param sentence: phrase a traiter
			:type sentence: string
			:return: parse de sentence
			:rtype: json
		"""
		return self.nlp.parse(sentence)

	def dependency_parse(self, sentence):
		"""
			def dependency_parse(self, sentence)
			------------------------------------
			
			retourne les dependances de l'analyse de corenlp
			
			:param sentence: phrase a traiter
			:type sentence: string
			:return: dependance de sentence
			:rtype: json
		"""
		return self.nlp.dependency_parse(sentence)

	def annotate(self, sentence):
		"""
			def annotate(self, sentence)
			----------------------------
			
			retourne les annotations de l'analyse de corenlp
			
			:param sentence: phrase a traiter
			:type sentence: string
			:return: annotation de sentence
			:rtype: json
		"""
		return json.loads(self.nlp.annotate(sentence, properties=self.props))

	@staticmethod
	def tokens_to_dict(_tokens):
		"""
			def tokens_to_dict(self, sentence)
			----------------------------------
			
			retourne la liste des tokens de l'analyse de corenlp (méthode interne)
			
			:param _tokens: attribut de l'objet
			:type _tokens: dictionnary
			:return: dictionnaire des tokens
			:rtype: dictionnary
		"""
		tokens = defaultdict(dict)
		for token in _tokens:
			tokens[int(token['index'])] = {
				'word': token['word'],
				'lemma': token['lemma'],
				'pos': token['pos'],
				'ner': token['ner']
		}
		return tokens
		
	def getTokens(self, sentence):
		"""
			def getTokens(self, sentence)
			-----------------------------
			
			retourne la liste des tokens de l'analyse de corenlp
			
			:param sentence: phrase a traiter
			:type sentence: string
			:return: dictionnaire des tokens
			:rtype: dictionnary
		"""
		tok = {}

		for s in self.annotate(sentence)['sentences']:
			for d in s['tokens']:
				tok[d['index']] = {'word' : d['originalText'], 'lemma' : d['lemma'], 'pos' : d['pos'], 'ner': d['ner']}
		return tok
		
	def segmente(self, sentence):
		"""
			def segmente(self, sentence)
			----------------------------
			
			retourne la liste des segments de l'analyse de corenlp
			
			:param sentence: phrase a traiter
			:type sentence: string
			:return: liste des segments de sentence
			:rtype: list
		"""
		
		dic = self.annotate(sentence)

		segments = []
		for s in dic['sentences']:
			seg = []
			for w in s['tokens']:
				seg.append(w['word'])
			segments.append(" ".join(seg))

		return segments
