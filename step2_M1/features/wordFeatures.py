#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module features/wordFeatures.py
# Author : SABLAYROLLES Louis
# Date : 11 / 06 / 17

# compute word features

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
		if w.lower() in ["who", "what", "why", "which", "whom", "whose", "where", "how"]:
			nbWhw += 1
	
	return nbWhw