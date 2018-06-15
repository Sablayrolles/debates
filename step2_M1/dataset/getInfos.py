#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module dataset/getInfos.py
# Author : SABLAYROLLES Louis
# Date : 11 / 06 / 17

# return infos of a debates

import xml.etree.ElementTree as ET
import re

def getInfosDebates(file):
	"""
		def getInfosDebates(file)
		-------------------------
		
		return infos of a debates
		
		:param file: file infos.xml in debates directory
		:type file: string
		:return: dictionnary of infos
		:rtype: dictionnary
	"""
	
	infos = {}
	f = open(file)
	sentences = f.readline()
	f.close()
	
	tree = ET.parse(file)
	root = tree.getroot()
	for child in root:
		# print("\tTag:",child.tag,"Text:",child.text)
		if child.tag == "language":
			infos["language"] = child.text
		if child.tag == "debateNum":
			infos["debateNum"] = child.text
		if child.tag == "country":
			infos["country"] = child.text
		if child.tag == "numberQuestion":
			infos["numberQuestion"] = child.text
		if child.tag == "date":
			infos["date"] = child.text
		if child.tag == "participant":
			for subchild in child.iterfind("./"):
				if subchild.tag == "presentator":
					infos["presentator"] = subchild.text
				if subchild.tag == "candidate":
					if "candidates" not in infos.keys():
						infos["candidates"] = [subchild.text]
					else:
						infos["candidates"].append(subchild.text)
	return infos

if __name__ == "__main__":
	infos = getInfosDebates("./usa/2016/1/infos.xml")
	print(infos)