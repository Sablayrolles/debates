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
	Module computeFeaturesLinear
	============================
	
	This module can be use to compute and save features that depend of others EDU on a computeFeatures
	
"""
counters = {}
def returnFeatures(data, preComputeFeatures, NB_PREV, NB_NEXT, featuresList, allNumbered=False):
	"""
		def returnFeatures(data, featuresList)
		--------------------------------------
		
		return dictionnary of features for an EDU
		
		:param data: data extract from saveData.py
		:type data: dictionnary
		:return: dictionnary of features for an EDU
		:rtype: dictionnary
	"""
	features = {}
	boolean = not(allNumbered)
	
	#-------------------------------------------------------------------------------------------------------------------------------
	#increasing counters
	global counters
	#topics
	if "nbEDUTopics" not in counters.keys() or counters["old_q"] != data[0]["question"]:
		counters["nbEDUTopics"] = 1
		counters["old_q"] = data[0]["question"]
	else:
		counters["nbEDUTopics"] += 1
	if "nb"+data[0]["emitter"]+"topic" not in counters.keys() or counters["old_q"] != data[0]["question"]:
		counters["nb"+data[0]["emitter"]+"topic"] = 1
	else:
		counters["nb"+data[0]["emitter"]+"topic"] += 1
		
	#segments
	if "old_speaker" not in counters.keys() or counters["old_q"] != data[0]["question"] or data[0]["emitter"] != counters["old_speaker"]:
		counters["old_speaker"] = data[0]["emitter"]
		counters["nbEDUSegment"] = 1
	else:
		counters["nbEDUSegment"] += 1
	#-------------------------------------------------------------------------------------------------------------------------------
	
	for f in featuresList:
		#tokens features
		if f == "as?":
			features["as?"] = tFeatures.asQuestionMark(data[0]["tokens"], boolean)
		if f == "nbTokSameEDUPrev":
			for i in range(NB_PREV):
				if data[-i] != None:
					features["nbTokSameEDUPrev:"+str(-i)] = tFeatures.nbSameTok(data[0]["tokens"], data[-i]["tokens"])
				else:
					features["nbTokSameEDUPrev:"+str(-i)] = 0
		if f == "nbTokSameEDUNext":
			for i in range(NB_NEXT):
				if data[i] != None:
					features["nbTokSameEDUNext:"+str(i)] = tFeatures.nbSameTok(data[0]["tokens"], data[i]["tokens"])
				else:
					features["nbTokSameEDUNext:"+str(i)] = 0
		#env
		if f == "positionInTopic":
			features["positionInTopic"] = counters["nbEDUTopics"]
		if f == "positionInSegment":
			features["positionInSegment"] = counters["nbEDUSegment"]
		if f == "nbEDUsaidBySpeakerInTopic":
			features["nbEDUsaidBySpeakerInTopic"] = counters["nb"+data[0]["emitter"]+"topic"]
		if f == "nbEDUsaidByOthersSpeakerInTopic":
			features["nbEDUsaidByOthersSpeakerInTopic"] = 0 
			for k in counters.keys():
				if "topic" in k and "nb" in k and data[0]["emitter"] not in k:
					features["nbEDUsaidByOthersSpeakerInTopic"] += counters[k]
	
	for k in preComputeFeatures[0].keys():
		features[k] = preComputeFeatures[0][k]
	return features

NB_FAITS = 0
def processEDULogReg(n, nbTT, NB_PREV, NB_NEXT):
	global NB_FAITS
	
	#calcul words
	data = {}
	data[0] = joblib.load("./data/"+str(n)+".data")
	for i in range(1,NB_PREV+1):
		try:
			with open("./data/"+str(n-i)+".data"): pass
			data[-i] = joblib.load("./data/"+str(n-i)+".data")
		except IOError:
			data[-i] = None
					
	for i in range(1, NB_NEXT+1):
		try:
			with open("./data/"+str(n+i)+".data"): pass
			data[i] = joblib.load("./data/"+str(n+i)+".data")
		except IOError:
			data[i] = None
	
	features = {}
	features[0] = joblib.load("./data/"+str(n)+".features")
	for i in range(1,NB_PREV+1):
		try:
			with open("./data/"+str(n-i)+".features"): pass
			features[-i] = joblib.load("./data/"+str(n-i)+".features")
		except IOError:
			features[-i] = None
					
	for i in range(1, NB_NEXT+1):
		try:
			with open("./data/"+str(n+i)+".features"): pass
			features[i] = joblib.load("./data/"+str(n+i)+".features")
		except IOError:
			features[i] = None
			
	print("Data Keys : ", data.keys())
	print("Features Keys : ", features.keys())
	f = returnFeatures(data, features, NB_PREV, NB_NEXT, ["nbTokSameEDUPrev", "nbTokSameEDUNext", "positionInTopic", "positionInSegment", "nbEDUsaidBySpeakerInTopic", "nbEDUsaidBySpeakerInTopic"], False)
	joblib.dump(f,"./data/"+str(f["num"])+".features");
	
	NB_FAITS += 1
	print('\033[1A'+"[Features] Computing features : ",NB_FAITS,"/",nbTT)
	
	return 0
	
def processEDUCRF(n, nbTT, NB_PREV, NB_NEXT):
	global NB_FAITS
	
	#calcul words
	data = {}
	data[0] = joblib.load("./data/"+str(n)+".data")
	for i in range(1,NB_PREV+1):
		try:
			with open("./data/"+str(n-i)+".data"): pass
			data[-i] = joblib.load("./data/"+str(n-i)+".data")
		except IOError:
			data[-i] = None
					
	for i in range(1, NB_NEXT+1):
		try:
			with open("./data/"+str(n+i)+".data"): pass
			data[i] = joblib.load("./data/"+str(n+i)+".data")
		except IOError:
			data[i] = None
	
	features = {}
	features[0] = joblib.load("./data/"+str(n)+".features")
	for i in range(1,NB_PREV+1):
		try:
			with open("./data/"+str(n-i)+".features"): pass
			features[-i] = joblib.load("./data/"+str(n-i)+".features")
		except IOError:
			features[-i] = None
					
	for i in range(1, NB_NEXT+1):
		try:
			with open("./data/"+str(n+i)+".features"): pass
			features[i] = joblib.load("./data/"+str(n+i)+".features")
		except IOError:
			features[i] = None
			
	f = returnFeatures(data, features, NB_PREV, NB_NEXT, ["nbTokSameEDUPrev", "nbTokSameEDUNext", "positionInTopic", "positionInSegment", "nbEDUsaidBySpeakerInTopic", "nbEDUsaidBySpeakerInTopic"])
	joblib.dump(f,"./data/"+str(f["num"])+".features");
	
	NB_FAITS += 1
	print('\033[1A'+"[Features] Computing features : ",NB_FAITS,"/",nbTT)
	
	return 0
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="\tModule computeFeaturesLinear\n\t===============\n\n\t\tThis module can be use to compute and save features that depend of others EDU on a computeFeatures")

	parser.add_argument("numFiles", metavar="nbFiles", type=int, help="Number of file .data to extract and save features (from saveData)")
	parser.add_argument("typeLearning", metavar="typeLearning", type=int, choices=[1, 2], help="Type of learning after\n\t1 : regression logistique\n\t 2 : CRF")
	parser.add_argument("-p", "--previous", metavar="previous", type=int, nargs="?", help="Nb core previous to see (default 2)")
	parser.add_argument("-n", "--next", metavar="next", type=int, nargs="?", help="Nb core next to see (default 1)")

	args = parser.parse_args()

	nbTT = int(args.numFiles) + 1
	typeLearn = int(args.typeLearning)
	if args.previous != None:
		NB_PREV = int(args.previous)
	else:
		NB_PREV = 2
	if args.next != None:
		NB_NEXT = int(args.next)
	else:
		NB_NEXT = 1
		
	print("Param : nbFiles="+str(nbTT))
	print("Param : typeLearn="+str(typeLearn)+" [1 : regression logistique, 2 : CRF]")
	print("Param : NB_PREV="+str(NB_PREV))
	print("Param : NB_NEXT="+str(NB_NEXT))
		
	features = joblib.load("./data/1.features")
	print("Features_already_existing:", features.keys())
		
	print("\n")
	nbTT = int(sys.argv[1])+1
	
	for i in range(1,nbTT):
		if typeLearn == 1:
			processEDULogReg(i, nbTT, NB_PREV, NB_NEXT)
		if typeLearn == 2:
			processEDUCRF(i, nbTT, NB_PREV, NB_NEXT)
	
	print("Computing ", int(sys.argv[1])+1, "files")
