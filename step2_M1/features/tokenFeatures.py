#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module features/tokenFeatures.py
# Author : SABLAYROLLES Louis
# Date : 11 / 06 / 17

# compute word features

def asQuestionMark(tokens):
	"""
		def asQuestionMark(tokens)
		--------------------------
		
		return if it as '?'
		
		:param tokens: list of tokens of the EDU
		:type tokens: list
		:return: 1 if as '?' / 0 else
		:rtype: int
	"""
	nbQMark = 0
	
	for t in tokens.keys():
		if tokens[t]["lemma"] == '?':
			nbQMark = 1 
	
	return nbQMark
	
def asExclamativeMark(tokens):
	"""
		def asExclamativeMark(tokens)
		-----------------------------
		
		return if it as '!'
		
		:param tokens: list of tokens of the EDU
		:type tokens: list
		:return: 1 if as '!' / 0 else
		:rtype: int
	"""
	nbExpl = 0
	
	for t in tokens.keys():
		if tokens[t]["lemma"] == '!':
			nbExpl = 1 
	
	return nbExpl
	
def asTriplePointsMark(tokens):
	"""
		def asTriplePointsMark(tokens)
		-----------------------------
		
		return if it as '...'
		
		:param tokens: list of tokens of the EDU
		:type tokens: list
		:return: 1 if as '...' / 0 else
		:rtype: int
	"""
	nb3Pt = 0
	
	for t in tokens.keys():
		if tokens[t]["lemma"] == '...':
			nb3Pt = 1 
	
	return nb3Pt
	
def nb1stPers(tokens):
	"""
		def nb1stPers(tokens)
		---------------------
		
		return nb of 1st pers pronom
		
		:param tokens: list of tokens of the EDU
		:type tokens: list
		:return: nb1stPers
		:rtype: int
	"""
	nb1stPers = 0
	
	for t in tokens.keys():
		if tokens[t]["lemma"] in ['I', 'my', "me", "mine", 'we', 'us', 'ours', 'our']:
			nb1stPers += 1 
	
	return nb1stPers
	
def nb2ndPers(tokens):
	"""
		def nb2ndPers(tokens)
		---------------------
		
		return nb of 2nd pers pronom
		
		:param tokens: list of tokens of the EDU
		:type tokens: list
		:return: nb2ndPers
		:rtype: int
	"""
	nb2ndPers = 0
	
	for t in tokens.keys():
		if tokens[t]["lemma"] in ['you', 'yours', 'yours', 'your']:
			nb2ndPers += 1 
	
	return nb2ndPers

def nb3rdSingPers(tokens):
	"""
		def nb3rdSingPers(tokens)
		-------------------------
		
		return nb of 3rd singular pers pronom
		
		:param tokens: list of tokens of the EDU
		:type tokens: list
		:return: nb3rdSingPers
		:rtype: int
	"""
	nb3rdSingPers = 0
	
	for t in tokens.keys():
		if tokens[t]["lemma"] in ['he', 'she', 'it', 'him', 'her', 'his', 'hers', 'its']:
			nb3rdSingPers += 1 
	
	return nb3rdSingPers
	
def nb3rdPluPers(tokens):
	"""
		def nb3rdPluPers(tokens)
		------------------------
		
		return nb of 3rd plural pers pronom
		
		:param tokens: list of tokens of the EDU
		:type tokens: list
		:return: nb3rdPluPers
		:rtype: int
	"""
	nb3rdPluPers = 0
	
	for t in tokens.keys():
		if tokens[t]["lemma"] in ['they', 'them', 'theirs', 'their']:
			nb3rdPluPers += 1 
	
	return nb3rdPluPers
	
def moyLengthTok(tokens):
	"""
		def moyLengthTok(tokens)
		------------------------
		
		return mean of length tokens
		
		:param tokens: list of tokens of the EDU
		:type tokens: list
		:return: mean of length tokens
		:rtype: float
	"""
	sum = 0
	
	for t in tokens.keys():
		sum += len(tokens[t]["lemma"])
	
	return float(sum) / float(len(tokens.keys()))
	
def nbNER(tokens):
	"""
		def nbNER(tokens)
		-----------------
		
		return nb Named Entities
		
		:param tokens: list of tokens of the EDU
		:type tokens: list
		:return: nb Named Entities
		:rtype: int
	"""
	nbNER = 0
	
	for t in tokens.keys():
		if len(tokens[t]["ner"]) > 3:
			nbNER += 1
	
	return nbNER