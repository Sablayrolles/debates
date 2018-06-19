#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module dataset/getData
# Author : SABLAYROLLES Louis
# Date : 07 / 05 / 17

# declaration of getData module to iterate on dataset files

file="./usa/2016/1/annotated/ac-aa/"

nbEDU = 0
types = {}

for num in [1,2,3,4,5,6,7,8,9]:
	name = file+str(num)+"-hand_parsed.aa"
	nFiles = 0
	tFiles = {}
	f = open(name,"r")
	for line in f.readlines():			
		if "<type>" in line: # and line[6:-8][0].isupper():
			if line[6:-8] not in ["default", "paragraph", "Dialogue", "Turn"]:
				nbEDU += 1
				nFiles += 1
				if line[6:-8] not in types.keys() and line[6:-8] != "Segment":
					types[line[6:-8]] = 1
				else:
					if line[6:-8] != "Segment":
						types[line[6:-8]] += 1
					else:
						if "Other" in types.keys():
							types["Other"] += 1
						else:
							types["Other"] = 1
							
				if line[6:-8] not in tFiles.keys() and line[6:-8] != "Segment":
					tFiles[line[6:-8]] = 1
				else:
					if line[6:-8] != "Segment":
						tFiles[line[6:-8]] += 1
					else:
						if "Other" in tFiles.keys():
							tFiles["Other"] += 1
						else:
							tFiles["Other"] = 1
	print("For file num",num)
	print("\t","nEDU:", nFiles)
	print("\t","types:", tFiles)
	for t in tFiles.keys():
		print("\t",t,":",tFiles[t]/nFiles*100, "%")
				

print("\n\nFor corpus")
print("nbEDU:", nbEDU)
print("types:", types)
for t in types.keys():
	print(t,":",types[t]/nbEDU*100, "%")
