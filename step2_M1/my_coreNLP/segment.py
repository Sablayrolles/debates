#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module my_coreNLP/segment
# Author : SABLAYROLLES Louis
# Date : 07 / 05 / 17

# own class to segment parsing of corenlp

import pickle
import pprint

"""
	Module segment
	===============
	
	This module can be use to segment parsing of corenlp.
	
"""

def links_words():
	return ["first", "firstly", "secondly", "thirdly", "then", "next", "actually", "whereas", "while", "unlike", "conversely", "otherwise", "although", "though", "whatever", "however", "unless", "whether", "yet", "still", "nevertheless", "nonetheless", "namely", "as", "because", "since", "so", "that", "therefore", "accordingly", "consequently", "thus", "hence", "eventually", "till", "until", "while", "whenever", "once", "meanwhile", "besides", "furthermore", "moreover", "also", "similarly", "but", "where"]
	
def cutWords(data_struct, list_words_cut):
	cutSentences = [[e['word'] for e in s["tokens"]] for s in data_struct["sentences"]]
	
	newSentences = []
	tmp = []
	for sentence in cutSentences:
		first = True
		for word in sentence:
			tmp.append(word)
			if word in list_words_cut and not first:
				newSentences.append(tmp)
				tmp = []
			first = False
		newSentences.append(tmp)
		tmp = []
	
	return newSentences

if __name__ == '__main__':
	data = pickle.load(open("segmentation.nlp", "rb"))
	pprint.pprint(data)
	
	print(cutWords(data,links_words()))
	#word pb: to, and, for