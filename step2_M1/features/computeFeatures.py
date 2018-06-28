#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module features/computeFeatures.py
# Author : SABLAYROLLES Louis
# Date : 11 / 06 / 17

# compute features

import joblib
import sys
sys.path.append("./")
sys.path.append("../")
import argparse

try:
	from . import wordFeatures as wFeatures
	from . import tokenFeatures as tFeatures
	from ..my_emoLex import emoLex as my_emoLex
except ImportError:
	import wordFeatures as wFeatures
	import tokenFeatures as tFeatures
	import my_emoLex.emoLex as my_emoLex
except SystemError:
	import wordFeatures as wFeatures
	import tokenFeatures as tFeatures
	import my_emoLex.emoLex as my_emoLex
	
"""
	Module computeFeatures
	======================
	
	This module can be use to compute and save features on a savedata
	
"""

def returnFeatures(data, featuresList, namesCandidates, emoLex, allNumbered=False):
	"""
		def returnFeatures(data, featuresList)
		--------------------------------------
		
		return dictionnary of features for an EDU
		
		:param data: data extract from saveData.py
		:type data: dictionnary
		:return: dictionnary of features for an EDU
		:rtype: dictionnary
	"""
	features = {"num": data["num"], "edu": data["edu"], "question": data["question"]}
	boolean = not(allNumbered)
	
	for f in featuresList:
	
		#words features
		if f == "nbWhWords":
			features["nbWhWords"] = wFeatures.nbWhWords(data["words"])
		if f == "namesCandidates":
			features["namesCandidates"] = wFeatures.namesCandidates(data["words"], namesCandidates)
		if f == "incise":
			features["incise"] = wFeatures.incise(data["words"])
		if f == "nbGalTerms":
			features["nbGalTerms"] = wFeatures.nbGalTerms(data["words"])
		if f == "nbNoGalTerms":
			features["nbNoGalTerms"] = wFeatures.nbNoGalTerms(data["words"])
			
		#tokens features	
		if f == "as?":
			features["as?"] = tFeatures.asQuestionMark(data["tokens"], boolean)
		if f == "as!":
			features["as!"] = tFeatures.asExclamativeMark(data["tokens"], boolean)
		if f == "as...":
			features["as..."] = tFeatures.asTriplePointsMark(data["tokens"], boolean)
		if f == "nb1stPers":
			features["nb1stPers"] = tFeatures.nb1stPers(data["tokens"])
		if f == "nb2ndPers":
			features["nb2ndPers"] = tFeatures.nb2ndPers(data["tokens"])
		if f == "nb3rdSingPers":
			features["nb3rdSingPers"] = tFeatures.nb3rdSingPers(data["tokens"])
		if f == "nb3rdPluPers":
			features["nb3rdPluPers"] = tFeatures.nb3rdSingPers(data["tokens"])
		if f == "moyLengthTok":
			features["moyLengthTok"] = tFeatures.moyLengthTok(data["tokens"])
		if f == "nbNER":
			features["nbNER"] = tFeatures.moyLengthTok(data["tokens"])
		if f == "nbTokens":
			features["nbTokens"] = tFeatures.nbTokens(data["tokens"])
		if f == "percentOfStopWords":
			features["percentOfStopWords"] = tFeatures.percentOfStopWords(data["tokens"])
		if f == "numberOfPositveEmotionWords":
			features["numberOfPositveEmotionWords"] = tFeatures.numberOfPositveEmotionWords(data["tokens"], emoLex)
		if f == "numberOfNegativeEmotionWords":
			features["numberOfNegativeEmotionWords"] = tFeatures.numberOfNegativeEmotionWords(data["tokens"], emoLex)
		if f == "numberOfBothEmotionWords":
			features["numberOfBothEmotionWords"] = tFeatures.numberOfBothEmotionWords(data["tokens"], emoLex)
		if f == "numberOfNeutralEmotionWords":
			features["numberOfNeutralEmotionWords"] = tFeatures.numberOfNeutralEmotionWords(data["tokens"], emoLex)
		if f == "moyEmotionWords":
			features["moyEmotionWords"] = tFeatures.moyEmotionWords(data["tokens"], emoLex)
			
		#env
		if f == "speakerNum":
			n = namesCandidates.copy()
			for i in range(len(n)):
				n[i] = n[i].lower()
			if data["emitter"].lower() not in n:
				features["speaker"] = 0
			else:
				features["speaker"] = n.index(data["emitter"].lower())+1
		if f == "speakerName" and not allNumbered:
			print("[Features] Incompatible parameter allNumbered and feature speakerName")
			features["speaker"] = data["emitter"]
			
	return features

NB_FAITS = 0
def processEDULogReg(n, nbTT, emoLex):
	global NB_FAITS
	
	NAMES =  ["Clinton", "Trump", "Holt", "Lester", "Donald", "Hillary"]
	#calcul words
	data = joblib.load("./data/"+str(n)+".data")
	f = returnFeatures(data, ["nbWhWords", "namesCandidates", "nbGalTerms", "nbNoGalTerms", "as?", "as!", "as...", "nb1stPers", "nb2ndPers", "nb3rdSingPers", "nb3rdPluPers", "moyLengthTok", "nbNER", "nbTokens", "percentOfStopWords", "numberOfPositveEmotionWords", "numberOfNegativeEmotionWords", "numberOfBothEmotionWords", "numberOfNeutralEmotionWords", "moyEmotionWords", "speakerNum"], NAMES, emoLex, False)
	joblib.dump(f,"./data/"+str(f["num"])+".features");
	
	NB_FAITS += 1
	print('\033[1A'+"[Features] Computing features : ",NB_FAITS,"/",nbTT)
	
	return 0
	
def processEDUCRF(n, nbTT, emoLex):
	global NB_FAITS
	
	NAMES =  ["Clinton", "Trump", "Holt", "Lester", "Donald", "Hillary"]
	#calcul words
	data = joblib.load("./data/"+str(n)+".data")
	f = returnFeatures(data, ["nbWhWords", "namesCandidates", "nbGalTerms", "nbNoGalTerms", "as?", "as!", "as...", "nb1stPers", "nb2ndPers", "nb3rdSingPers", "nb3rdPluPers", "moyLengthTok", "nbNER", "nbTokens", "percentOfStopWords", "numberOfPositveEmotionWords", "numberOfNegativeEmotionWords", "numberOfBothEmotionWords", "numberOfNeutralEmotionWords", "moyEmotionWords", "speakerNum"], NAMES, emoLex)
	joblib.dump(f,"./data/"+str(f["num"])+".features");
	
	NB_FAITS += 1
	print('\033[1A'+"[Features] Computing features : ",NB_FAITS,"/",nbTT)
	
	return 0
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="\tModule computeFeatures\n\t===============\n\n\t\tThis module can be use to compute and save features on a savedata computing on dataset")

	parser.add_argument("numFiles", metavar="nbFiles", type=int, help="Number of file .data to extract and save features (from saveData)")
	parser.add_argument("typeLearning", metavar="typeLearning", type=int, choices=[1, 2], help="Type of learning after\n\t1 : regression logistique\n\t 2 : CRF")
	parser.add_argument("-c", "--core", metavar="core", type=int, nargs="?", help="Nb core to execute (default 1)")

	args = parser.parse_args()

	nbTT = int(args.numFiles) + 1
	typeLearn = int(args.typeLearning)
	if args.core != None:
		NB_CORE = int(args.core)
	else:
		NB_CORE = 1
		
	print("Param : nbFiles="+str(nbTT))
	print("Param : NB_CORE="+str(NB_CORE))
	print("Param : typeLearn="+str(typeLearn)+" [1 : regression logistique, 2 : CRF]")
		
	data = joblib.load("./data/1.data")
	print("Infos:", data.keys())
		
	print("\n")
	nbTT = int(sys.argv[1])+1
	
	emoLex = my_emoLex.EmoLex("~/stageM1/debates/step2_M1/my_emoLex/english_EmoLex.csv")
	emoLex.load()
	emoLex.selectCols(["word", "positive", "negative"])
	
	if NB_CORE == 1:
		for i in range(1,nbTT):
			if typeLearn == 1:
				processEDULogReg(i, nbTT, emoLex)
			if typeLearn == 2:
				processEDUCRF(i, nbTT, emoLex)
	else:
		if typeLearn == 1:
			ret = joblib.Parallel(n_jobs=NB_CORE,verbose=5,backend="multiprocessing")(joblib.delayed(processEDULogReg)(i, nbTT, emoLex) for i in range(1,nbTT))
		if typeLearn == 2:
			ret = joblib.Parallel(n_jobs=NB_CORE,verbose=5,backend="multiprocessing")(joblib.delayed(processEDUCRF)(i, nbTT, emoLex) for i in range(1,nbTT))
	
	print("Computing ", int(sys.argv[1])+1, "files")
