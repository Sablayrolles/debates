#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module dataset/evaluate_type_paragraph
# Author : SABLAYROLLES Louis
# Date : 31 / 05 / 17

# comptage de chaque type d'EDU

import sys
sys.path.append("..")
import math

import getData
from my_coreNLP.test.data_sentences import tab

def distance(len1, len_moy):
	return math.fabs(len1-len_moy)

#calcul des tailles moyennes
lmoy = {}
nbPara = {}
dist = {}
for k in tab.keys():
	nbPara[k] = 0
	dist[k] = 0
	lmoy[k] = 0
	for p in tab[k]:
		lmoy[k] += len(p)
	lmoy[k] /= len(tab[k])

#iter file
for i in [1,2,3,4,5,6,7,8,9]:
	file = "C:\\Users\\louis\\Documents\\GitHub\\debates\\step2_M1\\dataset\\usa\\2016\\1\\hand-segmented\\"+str(i)+".txt"
	
	for s in getData.Sentences(file, "(^[A-Z]+: )"):
		l = len(s["sentences"])
		
		#calcul dist
		for k in lmoy.keys():
			dist[k] = distance(l, lmoy[k])
			
		nbPara[min(dist, key=dist.get)] += 1
			
		print(nbPara)