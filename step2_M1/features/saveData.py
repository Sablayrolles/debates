#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module dataset/evaluate_type_paragraph
# Author : SABLAYROLLES Louis
# Date : 31 / 05 / 17

# save date extract from corenlp

import sys
sys.path.append("..")
import joblib

import dataset.getData as getData
import my_coreNLP.parseNLP as parseNLP

def saveWords(data):
	"""
		def saveWords(data)
		-------------------
		
		add list of words to dictionnary of data of EDU / sentences
		
		:param data: dictionnary obtain with iterator in dataset.getData
		:type data: dictionary
	"""
	data["words"] = data["edu"]
	for e in [",", ".", "!", "--", "?", ";"]:
		data["words"] = data["words"].replace(e,"")
		
	data["words"] = data["words"].split()
	
	return data
	
nbEDU = 0
NLP = parseNLP.StanfordNLP();
for num in [1,2,3,4,5,6,7,8,9]:
		file = "../dataset/usa/2016/1/hand-segmented/"+str(num)+".txt"
		it = getData.Sentences(file, "(^[A-Z]+: )", num, "EDU", nbEDU);
		nbEDU = it.nbEDU()
		for s in it:
		
			#calcul words
			s = saveWords(s)
			
			s["tokens"] = NLP.getTokens(s["edu"]);
			s["dependencies"] = NLP.dependency_parse(s["edu"]);
			
			joblib.dump(s,"./data/"+str(s["num"])+".data");
			print(s)
			a = input()
