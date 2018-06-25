#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module features/wordFeatures.py
# Author : SABLAYROLLES Louis
# Date : 11 / 06 / 17

# compute word features

"""
	Module wordFeatures
	===================
	
	This module contains word's features
	
"""

try:
	from . import definitions as defs
except ImportError:
	import definitions as defs
except SystemError:
	import definitions as defs


def nbWhWords(words):
	"""
		def nbWhWords(words)
		--------------------
		
		return the number of wh words
		
		:param words: list of tokens of the EDU
		:type words: string list
		:return: nb of wh words
		:rtype: int
	"""
	nbWhw = 0
	
	for w in words:
		if w.lower() in defs.whWords:
			nbWhw += 1
	
	return nbWhw
	
def namesCandidates(words, names):
	"""
		def namesCandidates(words, names)
		---------------------------------
		
		return the number of names of candidates
		
		:param words: list of tokens of the EDU
		:param names: list of names of candidates
		:type words: string list
		:type names: string list
		:return: nb of names of candidates
		:rtype: int
	"""
	nbNames = 0
	
	for i in range(len(names)):
		names[i] = names[i].lower()
	
	for w in words:
		if w.lower() in names:
			nbNames += 1
	
	return nbNames
	
def incise(words):
	"""
		def incise(words)
		------------------
		
		return 0 if not incise(--) 1 else
		
		:param words: list of tokens of the EDU
		:type words: string list
		:return: 0 if not incise(--) 1 else
		:rtype: int
	"""
	incise = 0
	
	for w in words:
		if w.lower() == "--":
			incise = 1
	
	return incise
	
def nbGalTerms(words):
	"""
		def nbGalTerms(words)
		---------------------
		
		return the number of general terms
		
		:param words: list of tokens of the EDU
		:type words: string list
		:return: nb of general terms
		:rtype: int
	"""
	nbGal = 0
	
	for w in words:
		if "every" in w.lower():
			nbGal += 1
	
	return nbGal
	
def nbNoGalTerms(words):
	"""
		def nbGalTerms(words)
		---------------------
		
		return the number of no general terms
		
		:param words: list of tokens of the EDU
		:type words: string list
		:return: nb of no general terms
		:rtype: int
	"""
	nbNoGal = 0
	
	for w in words:
		if "no" in w.lower() and len(w.lower()) != 2:
			nbNoGal += 1
	
	return nbNoGal