#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module my_coreNLP/old_segment
# Author : SABLAYROLLES Louis
# Date : 09 / 05 / 17

# own class of segment parse of corenlp [set hidden temporary]

import pickle
import pprint

"""
	Module old_segment
	===============
	
	This module can be use to segment parsing of corenlp.
	
"""

def links_words():
	"""
		def links_words()
		------------------------------
		
		retourne la liste des links_words a traiter en anglais
		
		:return: liste des links_words en anglais a traiter
		:rtype: string list
	"""
	return ["first", "firstly", "secondly", "thirdly", "then", "next", "actually", "whereas", "while", "unlike", "conversely", "otherwise", "although", "though", "whatever", "however", "unless", "whether", "yet", "still", "nevertheless", "nonetheless", "namely", "as", "because", "since", "so", "that", "therefore", "accordingly", "consequently", "thus", "hence", "eventually", "till", "until", "while", "whenever", "once", "meanwhile", "besides", "furthermore", "moreover", "also", "similarly", "but", "where", "when"]
	
def list_words_SubjectVerb_cut():
	"""
		def list_words_SubjectVerb_cut()
		------------------------------
		
		retourne la liste des links_words a traiter en anglais qui nécessite un découpage de type Sujet-Verbe
		
		:return: liste des links_words en anglais a traiterqui nécessite un découpage de type Sujet-Verbe
		:rtype: string list
	"""
	return ["and", "to", "that", 'for', "when", "where", "so"]
	
def cutWords(data_struct, list_words_cut, list_words_SubjectVerb_cut):
	"""
		def cutWords(data_struct, list_words_cut, list_words_SubjectVerb_cut)
		---------------------------------------------------------------------
		
		retourne la liste des nouvelles phrases ainsi que la liste des données de corenlp en fonction de ces nouvelles phrases
		
		:param data_struct: structure de données du parseur corenlp
		:param list_words_cut: liste des mots où l'on doit absolument sectionner si pas premier mot de la phrase
		:param list_words_SubjectVerb_cut: liste des mots où l'on doit sectionner si Sujet + Verbe avant et apres
		:type data_struct: corenlp parsing struct
		:type list_words_cut: string list
		:type list_words_SubjectVerb_cut: string list
		:return: liste des nouvelles phrases ainsi que la liste des données de corenlp en fonction de ces nouvelles phrases
		:rtype: list, list
	"""
	cutSentences = [[e['word'] for e in s["tokens"]] for s in data_struct["sentences"]]
	posWords = [[(e['word'],e['pos']) for e in s["tokens"]] for s in data_struct["sentences"]]
	
	structWords = []
	for sentence in data_struct['sentences']:
		for data in sentence["tokens"]:
			structWords.append(data)
	
	newSentences = []
	tmp = []
	new_temp = []
	hasVerbBefore = False
	hasNounBefore = False
	inAfter = False
	hasVerbAfter = False
	hasNounAfter = False
	for sentence, sentencePos in zip(cutSentences, posWords):
		hasVerbBefore = False
		hasNounBefore = False
		inAfter = False
		hasVerbAfter = False
		hasNounAfter = False
		previous = None
		
		oldstate = {}
		first = True
		for word, pos in zip(sentence, sentencePos):			
			#on gère les pos
			if not inAfter:
				hasNounBefore = hasNounBefore or ('NN' in pos) or ('PRP' in pos)
				hasVerbBefore = hasVerbBefore or ('VB' in pos and pos not in ['VB', 'VBG', 'VBN'])
			else:
				hasNounAfter = hasNounAfter or ('NN' in pos) or ('PRP' in pos)
				hasVerbAfter = hasVerbAfter or ('VB' in pos and pos not in ['VB', 'VBG', 'VBN'])
			
			#on vient de passer le links_word donc on veut effectuer les tests apres
			if word in list_words_SubjectVerb_cut and not first and hasVerbBefore and previous not in list_words_SubjectVerb_cut:
				#on rencontre un link pb 
				if inAfter and previous not in list_words_SubjectVerb_cut: #on en a deja rencontré un et qui ne le précède pas de suite
					oldstate = [newSentences, tmp, new_temp, hasNounBefore, hasVerbBefore, hasNounAfter, hasVerbAfter, inAfter]
					newSentences.append(tmp+new_temp)
					tmp = []
					new_temp = []
					hasNounBefore = hasNounAfter
					hasVerbBefore = hasVerbAfter
					hasNounAfter = False
					hasVerbAfter = False
					inAfter = False
				else:
					inAfter = True
			
			if word in list_words_cut and not first and word not in list_words_SubjectVerb_cut: #on split sur les links_words
				if hasVerbBefore and hasVerbAfter:
					newSentences.append(new_temp)
					newSentences.append(tmp)
				else:
					if new_temp != []:
						newSentences.append(tmp+new_temp)
					else:
						newSentences.append(tmp)
				tmp = []
				new_temp = []
				hasVerbBefore = False
				hasNounBefore = False
				inAfter = False
				hasVerbAfter = False
				hasNounAfter = False	
				
			if not inAfter:
				tmp.append(word)
			else:
				new_temp.append(word)
			
			first = False
			
			# print("", "word:", word, "\n", "previous:", previous, "\n", "pos:", pos, "\n", "tmp:", tmp, "\n", "new_temp:", new_temp, "\n", "in pb link word : ", inAfter, "\nres:", newSentences, "\n")
			# print("hasNounBefore",hasNounBefore,"hasVerbBefore",hasVerbBefore,"hasNounAfter",hasNounAfter,"hasVerbAfter",hasVerbAfter)
			# a = input()
			
			previous = word
			
		#on split en fin de phrase
		if hasNounBefore and hasVerbBefore and hasVerbAfter:
			newSentences.append(new_temp)
			newSentences.append(tmp)
		else:
			if new_temp != []:
				newSentences.append(tmp+new_temp)
			else:
				newSentences.append(tmp)
		tmp = []
		new_temp = []
		hasVerbBefore = False
		hasNounBefore = False
		inAfter = False
		hasVerbAfter = False
		hasNounAfter = False
		
		struct = []
		i = 0
		for sentence in newSentences : 
			d = []
			for words in sentence:
				d.append(structWords[i])
				i += 1
			struct.append(d)
	
	return newSentences, struct

if __name__ == '__main__':
	data = pickle.load(open("segmentation.nlp", "rb"))
	
	res, struct = cutWords(data,links_words(), list_words_SubjectVerb_cut())
	# pprint.pprint(res)
	print(struct[0])
	
	for split in [" ".join(t) for t in res]:
		print(split)
