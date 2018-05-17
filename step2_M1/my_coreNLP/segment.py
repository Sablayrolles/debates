#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module my_coreNLP/segment
# Author : SABLAYROLLES Louis
# Date : 09 / 05 / 17

# own class of segment parse of corenlp

import pickle
import pprint
import re

"""
	Module segment
	===============
	
	This module can be use to segment parsing of corenlp.
	
"""

flksndflndsln = 0

def generateNamesGraph():
	global flksndflndsln
	
	flksndflndsln += 1

	return "s"+str(flksndflndsln)

class Ligne:
	def __init__(self, l):
		self.l = l
		
	def countBeginningSpace(self):
		n = 0
		while self.l[n] == " ":
			n += 1
		
		return n

	def formatStringGraph(self):
		nbopenparenthesis = self.l.count("(")
		nbcloseparenthesis = self.l.count(")")
		lig = self.l.strip()
		if nbopenparenthesis < nbcloseparenthesis:
			for i in range(nbcloseparenthesis-nbopenparenthesis):
				lig = lig[0:-1]
		if nbopenparenthesis > nbcloseparenthesis:
			for i in range(nbopenparenthesis-nbcloseparenthesis):
				lig += ")"

		return lig

	def getLemma(self):
		reg = re.compile('[A-Z]?[a-z\',]+')
		return reg.findall(self.l), " ".join(reg.findall(self.l)).strip()

	def removeMultiplesSpaces(self):
		while self.l.count("  ") > 0:
			self.l = self.l.replace("  ", " ")

		return self.l

class Parser:
	def __init__(self, parse):
		self.parse = parse

	def exportGraph(self):
		old = {}
		preced_level = 0

		nodes,edges = "",""
		for lig in self.parse.split('\n'):
			myL = Ligne(lig)
			level = int(myL.countBeginningSpace() / 2)
			old_l = lig
			lig = myL.formatStringGraph()

			name = generateNamesGraph()
			nodes += "\t"+name+'[label="'+lig+'"];\n'

			if level != 0:
				edges += "\t"+old[level-1]+" -> "+name+"\n"
				
			old[level] = name

		print("digraph G{\n"+nodes+"\n"+edges+"\n"+"}\n")

	def getDictGraph(self):
		old = {}
		preced_level = 0

		rac = []
		correspond = {}
		dependance = {}
		for lig in self.parse.split('\n'):
			myL = Ligne(lig)
			level = int(myL.countBeginningSpace() / 2)
			old_l = lig
			lig = myL.formatStringGraph()

			name = generateNamesGraph()
			correspond[name] = lig
			dependance[name] = []
			if level != 0:
				dependance[old[level-1]].append(name)
			else:
				rac.append(name)

			if 'SBAR' in lig:
				rac.append(name)

			old[level] = name

			print('('+str(level)+')', old_l)
		return correspond, dependance, rac

	def getDictSubGraph(self):
		names, edges, rac = self.getDictGraph()

		subsgraphs = {}
		for r in rac:
			subsgraphs[r] = {'nodes' : {r:names[r]}
							,'edges' : {r:edges[r]}}
			lnodestodo = subsgraphs[r]['edges'][r]
			while lnodestodo != []:
				n = lnodestodo.pop()
				if n not in rac:
					subsgraphs[r]['nodes'][n] = names[n]
					subsgraphs[r]['edges'][n] = edges[n]
					lnodestodo += edges[n]

		return subsgraphs

	def segmente(self):
		subg = self.getDictSubGraph()
		
		seg = []
		for r in sorted(subg.keys()):
			edu = ""
			for n in sorted(subg[r]['nodes'].keys()):
				myL = Ligne(subg[r]['nodes'][n])
				lems, joined = myL.getLemma()
				edu += " " + joined
			myL = Ligne(edu)
			seg.append(myL.removeMultiplesSpaces())

		return seg
		
	
if __name__ == '__main__':
	data = pickle.load(open("segmentation.nlp", "rb"))
	
	j = 0;
	for i in data['sentences']:
		print("j:",j)

		myP = Parser(i['parse'])
		correspond, dependance, rac = myP.getDictGraph()

		seg = myP.segmente()
		pprint.pprint(seg)

		j += 1
	
