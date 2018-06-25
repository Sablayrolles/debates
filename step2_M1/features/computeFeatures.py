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

NB_CORE = 4

try:
	from . import wordFeatures as wFeatures
	from . import tokenFeatures as tFeatures
	from ..my_emoLex import emoLex as emoLex
except ImportError:
	import wordFeatures as wFeatures
	import tokenFeatures as tFeatures
	import my_emoLex.emoLex as emoLex
except SystemError:
	import wordFeatures as wFeatures
	import tokenFeatures as tFeatures
	import my_emoLex.emoLex as emoLex
	
"""
	Module computeFeatures
	======================
	
	This module can be use to compute and save features on a savedata
	
"""

def returnFeatures(data, featuresList, namesCandidates, allNumbered=False):
	"""
		def returnFeatures(data, featuresList)
		--------------------------------------
		
		return dictionnary of features for an EDU
		
		:param data: data extract from saveData.py
		:type data: dictionnary
		:return: 1 if as '!' / 0 else
		:rtype: int
	"""
	features = {"num": data["num"], "edu": data["edu"], "question": data["question"]}
	boolean = not(allNumbered)
	emoLex = None
	
	for f in featuresList:
		if emoLex == "None" and "Emotion" in f:
			emoLex = my_emoLex.EmoLex()
			emoLex.load().selectCols(["word", "positive", "negative"])
	
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
			features["percentOfStopWords"] = tFeatures.percentOfStopWords(data["tokens"], emoLex)
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
def processEDULogReg(n, nbTT):
	global NB_FAITS
	
	NAMES =  ["Clinton", "Trump", "Holt", "Lester", "Donald", "Hillary"]
	#calcul words
	data = joblib.load("./data/"+str(n)+".data")
	f = returnFeatures(data, ["nbWhWords", "namesCandidates", "nbGalTerms", "nbNoGalTerms", "as?", "as!", "as...", "nb1stPers", "nb2ndPers", "nb3rdSingPers", "nb3rdPluPers", "moyLengthTok", "nbNER", "nbTokens", "percentOfStopWords", "numberOfPositveEmotionWords", "numberOfNegativeEmotionWords", "numberOfBothEmotionWords", "numberOfNeutralEmotionWords", "moyEmotionWords", "speakerNum"], NAMES)
	joblib.dump(f,"./data/"+str(f["num"])+".features");
	
	NB_FAITS += 1
	print('\033[1A'+"[Features] Computing features : ",NB_FAITS,"/",nbTT)
	
	return 0
	
def processEDUCRF(n, nbTT):
	global NB_FAITS
	
	NAMES =  ["Clinton", "Trump", "Holt", "Lester", "Donald", "Hillary"]
	#calcul words
	data = joblib.load("./data/"+str(n)+".data")
	f = returnFeatures(data, ["nbWhWords", "namesCandidates", "nbGalTerms", "nbNoGalTerms", "as?", "as!", "as...", "nb1stPers", "nb2ndPers", "nb3rdSingPers", "nb3rdPluPers", "moyLengthTok", "nbNER", "nbTokens", "percentOfStopWords", "numberOfPositveEmotionWords", "numberOfNegativeEmotionWords", "numberOfBothEmotionWords", "numberOfNeutralEmotionWords", "moyEmotionWords", "speakerNum"], NAMES)
	joblib.dump(f,"./data/"+str(f["num"])+".features");
	
	NB_FAITS += 1
	print('\033[1A'+"[Features] Computing features : ",NB_FAITS,"/",nbTT)
	
	return 0
	
if __name__ == '__main__':
	if len(sys.argv) != 3:
		print("Usage ",sys.argv[0]," nbTTEDUFiles method of extraction\n 1: for logistical reg \n 2: for crf\n")
		sys.exit(0)
		
	data = joblib.load("./data/1.data")
	print("Infos:", data.keys())
		
	print("\n")
	nbTT = int(sys.argv[1])+1
	
	if sys.argv[2] == "1":
		ret = joblib.Parallel(n_jobs=NB_CORE,verbose=5)(joblib.delayed(processEDULogReg)(i, nbTT) for i in range(1,nbTT))
	if sys.argv[2] == "2":
		ret = joblib.Parallel(n_jobs=NB_CORE,verbose=5)(joblib.delayed(processEDUCRF)(i, nbTT) for i in range(1,nbTT))
	
	print("Computing ", int(sys.argv[1])+1, "files")
