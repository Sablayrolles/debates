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
	return ["first", "firstly", "secondly", "thirdly", "then", "next", "actually", "whereas", "while", "unlike", "conversely", "otherwise", "although", "though", "whatever", "however", "unless", "whether", "yet", "still", "nevertheless", "nonetheless", "namely", "as", "because", "since", "so", "that", "therefore", "accordingly", "consequently", "thus", "hence", "eventually", "till", "until", "while", "whenever", "once", "meanwhile", "besides", "furthermore", "moreover", "also", "similarly", "but", "where", "when"]
	
def list_words_SubjectVerb_cut():
	return ["and", "to", "that", 'for', "when", "where", "so"]
	
def cutWords(data_struct, list_words_cut, list_words_SubjectVerb_cut):
	cutSentences = [[e['word'] for e in s["tokens"]] for s in data_struct["sentences"]]
	posWords = [[(e['word'],e['pos']) for e in s["tokens"]] for s in data_struct["sentences"]]
	
	print(cutSentences)
	#print(posWords)
	
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
				
			# if previous == 'to' and ('VB' in pos) and oldstate != {}:
				# newSentences, tmp, new_temp, hasNounBefore, hasVerbBefore, hasNounAfter, hasVerbAfter, inAfter = oldstate
				# oldstate = {}
				# del newSentences[-1]
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
	
	return newSentences

if __name__ == '__main__':
	data = pickle.load(open("segmentation.nlp", "rb"))
	#pprint.pprint(data)
	#print(data)
	
	res = cutWords(data,links_words(), list_words_SubjectVerb_cut())
	# pprint.pprint(res)
	
	for split in [" ".join(t) for t in res]:
		print(split)
