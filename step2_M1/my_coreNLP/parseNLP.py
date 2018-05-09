#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module my_coreNLP/parseNLP
# Author : SABLAYROLLES Louis
# Date : 07 / 05 / 17

# own class to interact with stanfordcorenlp java api

from stanfordcorenlp import StanfordCoreNLP
import logging
import json
import pickle
import segment

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
		def start(self) : start or restart the timer 
		def pause(self) : pause the timer
		def getTime(self) : return the actual elapse time without stopping the timer
		def stop(self) : stop the timer and return the elapse time
	"""
	def __init__(self, host='http://localhost', port=9000):
		"""
			def __init__(self, host='http://localhost', port=9000)
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
			
			retourne la liste des tokens de l'analyse de corenlp
			
			:param sentence: phrase a traiter
			:type sentence: string
			:return: liste des tokens de sentence
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
		dic = json.loads(self.nlp.annotate(sentence, properties = {'annotators':'ssplit,ner,pos','pipelineLanguage': 'en','outputFormat': 'json'}))
		
		pickle.dump(dic, open( "segmentation.nlp", "wb" ) )
		
		return segment.cutWords(dic, segment.links_words()
