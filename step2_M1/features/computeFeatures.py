#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module features/computeFeatures.py
# Author : SABLAYROLLES Louis
# Date : 11 / 06 / 17

# compute features

import joblib
import sys
sys.path.append("./")

import .wordFeatures as wFeatures
import .tokenFeatures as tFeatures

"""
	Module computeFeatures
	======================
	
	This module can be use to compute and save features on a savedata
	
"""

def returnFeatures(data, featuresList):
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
	
	for f in featuresList:
		#words features
		if f == "nbWhWords":
			features["nbWhWords"] = wFeatures.nbWhWords(data["words"])
			
		#tokens features	
		if f == "as?":
			features["as?"] = tFeatures.asQuestionMark(data["tokens"])
		if f == "as!":
			features["as!"] = tFeatures.asExclamativeMark(data["tokens"])
		if f == "as...":
			features["as..."] = tFeatures.asTriplePointsMark(data["tokens"])
		if f == "nb1stPers":
			features["nb1stPers"] = tFeatures.nb1stPers(data["tokens"])
		if f == "nb2ndPers":
			features["nb2ndPers"] = tFeatures.nb2ndPers(data["tokens"])
		if f == "nb3rdSingPers":
			features["nb3rdSingPers"] = tFeatures.nb3rdSingPers(data["tokens"])
		if f == "nb3rdPluPers":
			features["nb3rdPluPers"] = tFeatures.nb3rdSingPers(data["tokens"])
			
	return features
	
if __name__ == '__main__':
	for n in range(1,730):
		print("EDU num : ",n)
		
		data = joblib.load("./data/"+str(n)+".data")
		f = returnFeatures(data, ["nbWhWords", "as?", "as!", "as...", "nb1stPers", "nb2ndPers", "nb3rdSingPers", "nb3rdPluPers"])

		print(f)
		
		joblib.dump(f,"./data/"+str(f["num"])+".features");
