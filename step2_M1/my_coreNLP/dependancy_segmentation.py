#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module my_coreNLP/depenancy_segmentation
# Author : SABLAYROLLES Louis
# Date : 17 / 05 / 17

# own class of segment parse of corenlp using dependancy

import parseNLP

class Dependancy_segment:
	def __init__(self, annotate, dependancy): #annotate on one sentences
		self.annotate = annotate
		self.dependancy = dependancy

	def genereNodes(self):
	 	self.nodes = {}
		for i in self.annotate['sentences']:
			for j in i['tokens']:
				self.nodes[j['index']] = j['originalText']

		return self.nodes

	def genereEdges(self):
		self.edges = {}
		self.typesEdges = {}
		for i in self.dependancy:
			if i[1] not in self.edges.keys():
				self.edges[i[1]] = [i[2]]
			else:
				self.edges[i[1]].append(i[2])
			self.typesEdges[i[1]][i[2]] = i[3]
		return self.edges, self.typesEdges


if __name__ ==  "__main__":
	sNLP = parseNLP.StanfordNLP()

	sentence = "And when these people are going to put billions and billions of dollars into companies, and when they're going to bring $2.5 trillion back from overseas, where they can't bring the money back, because politicians like Secretary Clinton won't allow them to bring the money back, because the taxes are so onerous, and the bureaucratic red tape, so what -- is so bad."

	annotate = sNLP.annotate(sentence)
	dependancy = sNLP.depencancy_parse(sentence)

	print(annotate)
	print(dependancy)
	
	depSeg = Dependancy_segment(annotate, dependancy)
	print("Nodes:", depSeg.genereNodes())
	print("Edges:", depSeg.genereEdges())
