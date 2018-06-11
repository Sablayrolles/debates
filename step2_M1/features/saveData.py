#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module features/saveData.py
# Author : SABLAYROLLES Louis
# Date : 11 / 06 / 17

# save date extract from corenlp

import sys
sys.path.append("..")
import joblib

import dataset.getData as getData
import my_coreNLP.parseNLP as parseNLP

"""
	Module saveData
	===============
	
	This module can be use saveData of corenlp computing on dataset
	
"""

def saveWords(data):
	"""
		def saveWords(data)
		-------------------
		
		add list of words to dictionnary of data of EDU / sentences
		
		:param data: dictionnary obtain with iterator in dataset.getData
		:type data: dictionary
		:return: dictionnary for the feature extraction
		:rtype: dictionnary
	"""
	data["words"] = data["edu"]
	for e in [",", ".", "!", "--", "?", ";"]:
		data["words"] = data["words"].replace(e,"")
		
	data["words"] = data["words"].split()
	
	return data
	
def compute(dictEDU, NLP):
	"""
		def compute(dictEDU, NLP)
		-------------------------
		
		calc all for the feature extraction and return it in a dictionnary
		
		:param dictEDU: dictionnary obtain with iterator in dataset.getData
		:param NLP: corenlp object
		:type dictEDU: dictionary
		:type data: object
		:return: dictionnary for the feature extraction
		:rtype: dictionnary
	"""
	dictEDU = saveWords(dictEDU)
	dictEDU["tokens"] = NLP.getTokens(s["edu"])
	dictEDU["dependencies"] = NLP.dependency_parse(s["edu"])
	
	return dictEDU

if __name__ == "__main__":
	nbEDU = 0
	NLP = parseNLP.StanfordNLP();
	for num in [1,2,3,4,5,6,7,8,9]:
		file = "../dataset/usa/2016/1/hand-segmented/"+str(num)+".txt"
		it = getData.Sentences(file, "(^[A-Z]+: )", num, "EDU", nbEDU);
		nbEDU = it.nbEDU()
		for s in it:
		
			#calcul words
			s = compute(s, NLP)
			
			joblib.dump(s,"./data/"+str(s["num"])+".data");
			print(s)
				
