#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module dataset/getData
# Author : SABLAYROLLES Louis
# Date : 07 / 05 / 17

# declaration of getData module to iterate on dataset files

file="C:\\Users\\louis\\Documents\\GitHub\\debates\\step2_M1\\dataset\\usa\\2016\\1\\output\\ac-aa\\"

nbEDU = 0
types = {}

for num in [1,2,3,4,5,6,7,8,9]:
	name = file+str(num)+"-hand_parsed.aa"
	
	f = open(name,"r")
	for line in f.readlines():
		if "<unit" in line:
			nbEDU += 1
			
		if "<type>" in line and line[6:-8][0].isupper():
			if line[6:-8] not in types.keys():
				types[line[6:-8]] = 1
			else:
				types[line[6:-8]] += 1
				

print("nbEDU:", nbEDU)
print("types:", types)
for t in types.keys():
	print(t,":",types[t]/nbEDU*100, "%")