#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module my_coreNLP/test/depenancy_segmentation
# Author : SABLAYROLLES Louis
# Date : 17 / 05 / 17

# own class of segment parse of corenlp using dependancy

from ast import literal_eval

f = open("../dependancy_graph/correspond", "r")

def listrem():
	return ["advcl", "ccomp", "expl", "parataxis", "pcomp", "prepc", "rcmod"]
	
def removeEdges(edges, attrib, list_rem=listrem()):
	heads = [0] #listes des têtes des propositions
	for node1, edge in edges.items():
		for node2 in edge:
			if attrib[node1][node2] in list_rem:
				print(node1,node2,attrib[node1][node2], "deleted")
				heads.append(node1)
				edges[node1].remove(node2)
				del attrib[node1][node2]
				
	return edges, attrib, heads

for l in f.readlines():
	fic = l.split(" : ")[0]
	sentence = l.split(" : ")[1]
	print("Sentence : ", sentence)
	
	fo = open("../dependancy_graph/nodes_"+fic, "r")
	nodes = fo.read() 
	fo.close()

	fo = open("../dependancy_graph/edges_"+fic, "r")
	a = fo.read()
	edges, edges_attributes = literal_eval(a)[0], literal_eval(a)[1]
	fo.close()
	
	edges, edges_attributes, heads = removeEdges(edges, edges_attributes) # TO ADD TO DEPENDANCY PARSE
	
	print("Nodes", nodes)
	print("Edges", edges)
	print("Edges attrib", edges_attributes)
	print("Heads", heads)
	
f.close()