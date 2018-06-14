#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module dataset/test-parse-xml
# Author : SABLAYROLLES Louis
# Date : 12 / 06 / 17

# comptage de chaque type d'EDU

import xml.etree.ElementTree as ET
import re

def getTypes1stdebate(repertory, number, entete_to_split="([0-9]+ : [A-Z]+ : )"):
	"""
		def getTypes1stdebate(repertory, number, entete_to_split="(^[A-Z]+: )")
		----------------------------------------------------------------------
		
		return all types for the an annoted file .aa and .ac
		:param repertory: repertory of .aa and .ac files
		:param number: number of question in the debate
		:param entete_to_split: split entete emitter
		:type repertory: string
		:type number: int
		:type entete_to_split: string
		:return: dictionnary of types indexed by (numfile, sentences)
		:rtype: dictionnary
	"""
	
	types = {}
	t = []
	for i in range(1,number+1):
		# print("Parsing q",i)
		file = repertory+str(i)+"-hand_parsed.aa"
		f = open(repertory+str(i)+"-hand_parsed.ac")
		sentences = f.readline()
		f.close()
		
		tree = ET.parse(file)
		root = tree.getroot()
		for child in root:
			if child.tag == "unit":
				# print("n1:",child.tag)
				for subchild in child.iterfind("./"):
					# print("\tn2:",subchild.tag)
					if subchild.tag == "characterisation":
						for subsubchild in subchild.iterfind("./"):
							# print("\t\tn3:",subsubchild.tag)
							if subsubchild.tag == "type":
								type = subsubchild.text
					if subchild.tag == "positioning":
						for subsubchild in subchild.iterfind("./"):
							# print("\t\tn3:",subsubchild.tag)
							if subsubchild.tag == "start":
								for subsubsubchild in subsubchild.iterfind("./"):
									# print("\t\t\tn4:",subsubsubchild.tag)
									start = subsubsubchild.get("index")
							if subsubchild.tag == "end":
								for subsubsubchild in subsubchild.iterfind("./"):
									# print("\t\t\tn4:",subsubsubchild.tag)
									stop = subsubsubchild.get("index")
				# print("type:", type, "start:", start, "stop:", stop)
				if type.lower() not in ['paragraph', 'turn', 'default', 'dialogue']:
					txt = sentences[int(start):int(stop)]
					if type not in t:
						t.append(type)
					# print(re.sub(entete_to_split, '', txt))
					if type.lower() == 'segment:
						type = 'Others'
					types[(i, re.sub(entete_to_split, '', txt))] = type

	return types, t

if __name__ == "__main__":
	data, t = getTypes1stdebate("./usa/2016/1/output/ac-aa/", 9)
	print(data)
	print("	nbTT:",len(data.keys()))
	print("types: ", t)