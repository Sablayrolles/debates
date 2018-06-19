#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module dataset/test-parse-xml
# Author : SABLAYROLLES Louis
# Date : 12 / 06 / 17

# comptage de chaque type d'EDU

import xml.etree.ElementTree as ET
import re
import joblib

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
	numEDU = 0
	for i in range(1,number+1):
		print("Parsing q",i)
		file = repertory+str(i)+"-hand_parsed.aa"
		f = open(repertory+str(i)+"-hand_parsed.ac")
		sentences = f.readline()
		f.close()
		
		d = {}
		tree = ET.parse(file)
		root = tree.getroot()
		typ = {}
		emitter = "Unknown"
		for child in root:
			if child.tag == "unit":
				# print("n1:",child.tag)
				type = None
				start = None
				stop = None
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
				if type != None and start != None and stop != None:
					# print("type:", type, "start:", start, "stop:", stop)
					#if type not in ["default", "paragraph", "Dialogue", "Turn"]:
					txt = sentences[int(start):int(stop)]
					# print(re.sub(entete_to_split, '', txt))
					if type == "Turn":
						m = re.search("( [A-Z]+[ ]+: )", txt)
						try:
							emmiter = m.group(0)
						except AttributeError:
							print(txt)
							a = input()

					if type not in ["Dialogue", "Turn", "paragraph"]:
						numEDU += 1	
						s={"num":numEDU, "emitter": emitter, "question": i, "edu": txt}
						joblib.dump(s,"../features/data/"+str(s["num"])+".info");
						if type in ["default", "Segment"]:
							type = 'Other'
						if type not in t:
							t.append(type)
						if type not in typ.keys():
							typ[type] = 1
						else:
							typ[type] += 1
						types[(i, re.sub(entete_to_split, '', txt))] = type
	print("Found : ", numEDU, "EDUs and save their infos")
	return types, t, numEDU

if __name__ == "__main__":
	data, t, nb = getTypes1stdebate("./usa/2016/1/annotated/ac-aa/", 9)
	print("	nbTT:",len(data.keys()))
	print("types: ", t)
	v = list(data.values())
	for k in t:
		print(k, ":", v.count(k))
	sys.exit(nb)
