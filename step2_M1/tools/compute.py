#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module tools/compute
# Author : SABLAYROLLES Louis
# Date : 28 / 05 / 17

# computre rpf over 3 category

import RappelPrecisionFMesure as rpf

rpfSentences = rpf.FScores(["small", "medium", "long"])
rpfPunct = rpf.FScores(["small", "medium", "long"])

for i in ["small", "medium", "long"]:
	continu = " "
	while continu != "":
		for j in ["LinksWords"]:
			print(i,j)
			if j == "Sentences":
				rpfSentences.saisieScore(i)
			else:
				rpfPunct.saisieScore(i)
		print("Another? (blank to stop)")
		continu = input()
		
for i in ["small", "medium", "long"]:
	for j in ["LinksWords"]:
		print("-------------\n",i,j)
		if j == "Sentences":
			print("p:",rpfSentences.getMoyPrecision(i))
			print("r:",rpfSentences.getMoyRappel(i))
		else:
			print("p:",rpfPunct.getMoyPrecision(i))
			print("r:",rpfPunct.getMoyRappel(i))