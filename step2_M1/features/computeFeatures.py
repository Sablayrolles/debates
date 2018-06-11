#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module features/computeFeatures.py
# Author : SABLAYROLLES Louis
# Date : 11 / 06 / 17

# compute features

import joblib

import wordFeatures as wFeatures
import tokenFeatures as tFeatures

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
	features = {"num": data["num"]}
	
	for f in featuresList:
		if f == "nbWhWords":
			features["nbWhWords"] = wFeatures.nbWhw(data["words"])
		if f == "as?":
			features["as?"] = tFeatures.asQuestionMark(data["tokens"])
		if f == "as!":
			features["as!"] = tFeatures.asExclamativeMark(data["tokens"])
		if f == "as...":
			features["as..."] = tFeatures.asTriplePointsMark(data["tokens"])
			
	return features
	
for n in range(1,730):
	print("EDU num : ",n)
	
	data = joblib.load("./data/"+str(n)+".data")
	print(data.keys())
	
	a=input()