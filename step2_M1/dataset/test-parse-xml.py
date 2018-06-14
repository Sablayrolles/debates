#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module dataset/test-parse-xml
# Author : SABLAYROLLES Louis
# Date : 12 / 06 / 17

# comptage de chaque type d'EDU

import xml.etree.ElementTree as ET

types = {}
for i in [1,2,3,4,5,6,7,8,9]:
	file = "./usa/2016/1/annotated/ac-aa/"+str(i)+"-hand_parsed.aa"
	
	tree = ET.parse(file)
	root = tree.getroot()
	for child in root:
		if child.tag == "unit":
			print("n1:",child.tag)
			for subchild in child.iterfind("./"):
				print("\tn2:",subchild.tag)
				if subchild.tag == "characterisation":
					for subsubchild in subchild.iterfind("./"):
						print("\t\tn3:",subsubchild.tag)
						if subsubchild.tag == "type":
							type = subsubchild.text
				if subchild.tag == "positioning":
					for subsubchild in subchild.iterfind("./"):
						print("\t\tn3:",subsubchild.tag)
						if subsubchild.tag == "start":
							for subsubsubchild in subsubchild.iterfind("./"):
								print("\t\t\tn4:",subsubsubchild.tag)
								start = subsubsubchild.get("index")
						if subsubchild.tag == "end":
							for subsubsubchild in subsubchild.iterfind("./"):
								print("\t\t\tn4:",subsubsubchild.tag)
								stop = subsubsubchild.get("index")
			print("type:", type, "start:", start, "stop:", stop)
			if type.lower() not in ['paragraph', 'dialogue', 'turn', 'segment', 'default']:
				types[(i, start, stop)] = type

print("types:", types)				
	