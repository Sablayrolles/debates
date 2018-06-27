#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module features/tokenFeatures.py
# Author : SABLAYROLLES Louis
# Date : 11 / 06 / 17

# compute word features

"""
	Module tokenFeatures
	====================
	
	This module contains tokens's features
	
"""

try:
	from . import definitions as defs
except ImportError:
	import definitions as defs
except SystemError:
	import definitions as defs

def asQuestionMark(tokens, boolean=True):
	"""
		def asQuestionMark(tokens, boolean=True)
		----------------------------------------
		
		return if it as '?'
		
		:param tokens: list of tokens of the EDU
		:type tokens: list
		:param boolean: if you want return to be a bool
		:type boolean: bool
		:return: 1 / True if as '?' - 0 / False else
		:rtype: int / bool
	"""
	if boolean:
		nbQMark = False
	else:
		nbQMark = 0
	
	for t in tokens.keys():
		if tokens[t]["lemma"] == '?':
			if boolean:
				nbQMark = True
			else:
				nbQMark = 1
	
	return nbQMark
	
def asExclamativeMark(tokens, boolean=True):
	"""
		def asExclamativeMark(tokens, boolean=True)
		-------------------------------------------
		
		return if it as '!'
		
		:param tokens: list of tokens of the EDU
		:type tokens: list
		:param boolean: if you want return to be a bool
		:type boolean: bool
		:return: 1 / True if as '!' - 0 / False else
		:rtype: int / bool
	"""
	nbExpl = 0
	
	for t in tokens.keys():
		if tokens[t]["lemma"] == '!':
			if boolean:
				nbQMark = True
			else:
				nbQMark = 1
			nbExpl = 1 
	
	return nbExpl
	
def asTriplePointsMark(tokens, boolean=True):
	"""
		def asTriplePointsMark(tokens, boolean=True)
		--------------------------------------------
		
		return if it as '...'
		
		:param tokens: list of tokens of the EDU
		:type tokens: list
		:param boolean: if you want return to be a bool
		:type boolean: bool
		:return: 1 / True if as '...' - 0 / False else
		:rtype: int / bool
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
		if tokens[t]["lemma"] in defs.pronom1stPers:
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
		if tokens[t]["lemma"] in defs.pronom2ndPers:
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
		if tokens[t]["lemma"] in defs.pronom3rdSingPers:
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
		if tokens[t]["lemma"] in defs.pronom3rdPluPers:
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
	
	if len(tokens.keys()) != 0:
		return float(sum) / float(len(tokens.keys()))
	else:
		return 0
	
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

def nbTokens(tokens):
	"""
		def nbTokens(tokens)
		--------------------
		
		return nb tokens
		
		:param tokens: list of tokens of the EDU
		:type tokens: list
		:return: nb tokens
		:rtype: int
	"""
	
	return len(tokens)
	
def percentOfStopWords(tokens):
	"""
		def percentOfStopWords(tokens)
		------------------------------
		
		return the percent of stop words
		
		:param tokens: list of tokens of the EDU
		:type tokens: list
		:return: percent of stop words
		:rtype: float
	"""
	sum = 0
	
	for t in tokens.keys():
		if tokens[t]["lemma"].lower() in defs.stopWords:
			sum += 1
	
	if len(tokens.keys()) != 0:
		return float(sum) / float(len(tokens.keys()))
	else:
		return 0
		
def numberOfPositveEmotionWords(tokens, emoLex):
	"""
		def numberOfPositveEmotionWords(tokens, emoLex)
		-----------------------------------------------
		
		return the number of positive words
		
		:param tokens: list of tokens of the EDU
		:param emoLex: emoLex object
		:type tokens: list
		:type emoLex: object
		:return: number of positive words
		:rtype: int
	"""
	nbPositive = 0
	
	for t in tokens.keys():
		if emoLex.getVals(tokens[t]["lemma"].lower(), "positive") == 1:
			nbPositive += 1
	
	return nbPositive
	
def numberOfNegativeEmotionWords(tokens, emoLex):
	"""
		def numberOfNegativeEmotionWords(tokens, emoLex)
		------------------------------------------------
		
		return the number of negative words
		
		:param tokens: list of tokens of the EDU
		:param emoLex: emoLex object
		:type tokens: list
		:type emoLex: object
		:return: number of negative words
		:rtype: int
	"""
	nbNegarive = 0
	
	for t in tokens.keys():
		if emoLex.getVals(tokens[t]["lemma"].lower(), "negative") == 1:
			nbNegarive += 1
	
	return nbNegarive
	
def numberOfBothEmotionWords(tokens, emoLex):
	"""
		def numberOfBothEmotionWords(tokens, emoLex)
		--------------------------------------------
		
		return the number of positive and negative words
		
		:param tokens: list of tokens of the EDU
		:param emoLex: emoLex object
		:type tokens: list
		:type emoLex: object
		:return: number of positive and negative words
		:rtype: int
	"""
	nbBoth = 0
	
	for t in tokens.keys():
		if emoLex.getVals(tokens[t]["lemma"].lower(), "positive") == 1 and emoLex.getVals(tokens[t]["lemma"].lower(), "negative") == 1:
			nbBoth += 1
	
	return nbBoth
	
def numberOfNeutralEmotionWords(tokens, emoLex):
	"""
		def numberOfNeutralEmotionWords(tokens, emoLex)
		-----------------------------------------------
		
		return the number of neutral words
		
		:param tokens: list of tokens of the EDU
		:param emoLex: emoLex object
		:type tokens: list
		:type emoLex: object
		:return: number of neutral words
		:rtype: int
	"""
	nbNeutral = 0
	
	for t in tokens.keys():
		if emoLex.getVals(tokens[t]["lemma"].lower(), "positive") == 0 and emoLex.getVals(tokens[t]["lemma"].lower(), "negative") == 0:
			nbNeutral += 1
	
	return nbNeutral
	
def moyEmotionWords(tokens, emoLex):
	"""
		def moyEmotionWords(tokens, emoLex)
		-----------------------------------
		
		return the moy of emotion words
		
		:param tokens: list of tokens of the EDU
		:param emoLex: emoLex object
		:type tokens: list
		:type emoLex: object
		:return: moy of emotion words
		:rtype: float
	"""
	sum = float(numberOfPositveEmotionWords(tokens, emoLex)) - float(numberOfNegativeEmotionWords(tokens, emoLex)) + 0.5 * float(numberOfBothEmotionWords(tokens, emoLex))
	
	if len(tokens.keys()) != 0:
		return float(sum) / float(len(tokens.keys()))
	else:
		return 0
		
def nbSameTok(tokens1, tokens2):
	"""
		def nbSameTok(tokens1, tokens2)
		-------------------------------
		
		return the moy of emotion words
		
		:param tokens1: list of tokens of an EDU
		:param tokens2: list of tokens of an EDU
		:type tokens1: list
		:type tokens2: list
		:return: nb tok idem
		:rtype: float
	"""
	nbSame = 0
	
	tab1 = []
	for t in tokens1.keys():
		tab1.append(tokens[t]["lemma"])
	tab2 = []
	for t in tokens2.keys():
		tab2.append(tokens[t]["lemma"])
	
	for i in tab1:
		if tab2.count(i) != 0:
			nbSame += 1
	
	return nbSame