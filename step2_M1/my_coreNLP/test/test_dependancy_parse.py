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

def formatGraph(nodes, edges):
	for node in nodes.keys():
		if node not in edges.keys():
			edges[node] = []
	
	return edges

def bfs(G,s): #parcours en profondeur
	couleur = dict()
	for x in G : couleur[x] = 'blanc'
	P = dict()
	P[s] = None
	couleur[s] = 'gris'
	Q = [s]
	while Q:
		u = Q[0]
		for v in G[u]:
			if couleur[v] == 'blanc':
				P[v] = u
				couleur[v] = 'gris'
				Q.append(v)
		Q.pop(0)
		couleur[u] = 'noir'
	return P

def genereSubGraphs(nodes, edges, attrib, heads):
	subgraphs = []
	graph = formatGraph(nodes, edges)
	print(nodes, edges, attrib)
	for h in heads:
		n = {}
		e = {}
		a = {}
		lnodes = bfs(graph, h)
		for node in lnodes:
			n[node] = nodes[node]
			for node2 in edges[node]:
				if node2 in lnodes:
					if node not in e.keys():
						e[node] = [node2]
						a[node] = {node2:attrib[node][node2]}
					else:
						e[node].append(node2)
						a[node][node2] = attrib[node][node2]
		newNodes = {}
		for k,v in sorted(n.items(), key=lambda t: t[0]):
			if k != 0:
				newNodes[k] = v
		subgraphs.append({'nodes':newNodes, 'edges':e, 'attrib': a})
	return subgraphs

def genereSegments(subgraphs):
	seg = []
	for graph in subgraphs:
		txt = ""
		for n in graph['nodes'].keys():
			txt += " "+graph['nodes'][n]
		seg.append(txt.strip())
	return seg

for l in f.readlines():
	fic = l.split(" : ")[0]
	sentence = l.split(" : ")[1]
	print("----------------------------------------------------------------------------------------------------\nSentence : ", sentence)
	
	fo = open("../dependancy_graph/nodes_"+fic, "r")
	nodes = literal_eval(fo.read())
	nodes[0] = 'ROOT'
	fo.close()

	fo = open("../dependancy_graph/edges_"+fic, "r")
	a = fo.read()
	edges, edges_attributes = literal_eval(a)[0], literal_eval(a)[1]
	fo.close()
	
	edges, edges_attributes, heads = removeEdges(edges, edges_attributes) # TO ADD TO DEPENDANCY PARSE
	
	subgraphs = genereSubGraphs(nodes, edges, edges_attributes, heads)
	#print("Subgraphs : ", subgraphs)# TO ADD TO DEPENDANCY PARSE
	print("\nSegments : ", genereSegments(subgraphs),"\n----------------------------------------------------------------------------------------------------\n")
f.close()