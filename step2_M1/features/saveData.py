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
import dataset.getInfos as getInfos
import my_coreNLP.parseNLP as parseNLP

NB_CORE = 8

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
	dictEDU["tokens"] = NLP.getTokens(dictEDU["edu"])
	dictEDU["dependencies"] = NLP.dependency_parse(dictEDU["edu"])
	
	return dictEDU

NB_FAITS = 0
def processEDU(n, nbTT):
	global NB_FAITS
	
	#calcul words
	s = joblib.load("./data/"+str(n)+".info")
	s = compute(s, NLP)
	joblib.dump(s,"./data/"+str(n)+".data");
	
	NB_FAITS += 1
	print('\033[1A'+"[Features] Saving infos :",NB_FAITS,"/",nbTT)
	
	return 0
	
if __name__ == "__main__":
	nbEDU = 0
	NLP = parseNLP.StanfordNLP();
	infos = getInfos.getInfosDebates("../dataset/usa/2016/1/infos.xml")
	nb = 0
	if len(sys.argv) != 2:
		print("Usage ", sys.argv[0], "nbfichier.info in features/data")
		
	print("\n")
	nbTT = int(sys.argv[1])+1
	
	ret = joblib.Parallel(n_jobs=NB_CORE)(joblib.delayed(processEDU)(i, nbTT) for i in range(1,nbTT))
	
	print("Extracted ", int(sys.argv[1])+1, "files")
				
