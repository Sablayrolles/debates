#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module my_coreNLP/depenancy_segmentation
# Author : SABLAYROLLES Louis
# Date : 17 / 05 / 17

# own class of segment parse of corenlp using dependancy

import parseNLP
import random

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
			if i[1] not in self.typesEdges.keys():
				self.typesEdges[i[1]] = {i[2] : i[0]}
			else:
				self.typesEdges[i[1]][i[2]] = i[0]
		return self.edges, self.typesEdges


if __name__ ==	"__main__":
	sNLP = parseNLP.StanfordNLP()

	sentences = [ "And when these people are going to put billions and billions of dollars into companies, and when they're going to bring $2.5 trillion back from overseas, where they can't bring the money back, because politicians like Secretary Clinton won't allow them to bring the money back, because the taxes are so onerous, and the bureaucratic red tape, so what -- is so bad." , "And I think probably he's not all that enthusiastic about having the rest of our country see what the real reasons are, because it must be something really important, even terrible, that he's trying to hide","When you have your staff taking the Fifth Amendment, taking the Fifth so they're not prosecuted, when you have the man that set up the illegal server taking the Fifth, I think it's disgraceful","Unfortunately, race still determines too much, often determines where people live, determines what kind of education in their public schools they can get, and, yes, it determines how they're treated in the criminal justice system.","I think maybe there's a political reason why you can't say it, but I really don't believe -- in New York City, stop-and-frisk, we had 2,200 murders, and stop-and-frisk brought it down to 500 murders.","But, remember, Donald started his career back in 1973 being sued by the Justice Department for racial discrimination because he would not rent apartments in one of his developments to African-Americans, and he made sure that the people who worked for him understood that was the policy.","But I like to remember what Michelle Obama said in her amazing speech at our Democratic National Convention: When they go low, we go high.","In Palm Beach, Florida, tough community, a brilliant community, a wealthy community, probably the wealthiest community there is in the world, I opened a club and no discrimination against African- Americans, against Muslims, against anybody.","Whether that was Russia, whether that was China, whether it was another country, we don't know, because the truth is, under President Obama we've lost control of things that we used to have control over.","He actually advocated for the actions we took in Libya and urged that Gadhafi be taken out, after actually doing some business with him one time. George W. Bush made the agreement about when American troops would leave Iraq, not Barack Obama.","Donald has consistently insulted Muslims abroad, Muslims at home, when we need to be cooperating with Muslim nations and with the American Muslim community.","I said, and very strongly, NATO could be obsolete, because -- and I was very strong on this, and it was actually covered very accurately in the New York Times, which is unusual for the New York Times, to be honest -- but I said, they do not focus on terror.","And that was -- believe me -- I'm sure I'm not going to get credit for it -- but that was largely because of what I was saying and my criticism of NATO.","Like when I did an interview with Howard Stern, very lightly, first time anyone's asked me that, I said, very lightly, I don't know, maybe, who knows?","And Sean Hannity said -- and he called me the other day -- and I spoke to him about it -- he said you were totally against the war, because he was for the war."]

	for sentence in sentences:
		annotate = sNLP.annotate(sentence)
		dependancy = sNLP.dependency_parse(sentence)
		chars = "".join([random.choice(list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefhijklmnopqrstuvwxyz0123456789")) for i in range(15)])

		depSeg = Dependancy_segment(annotate, dependancy)
	
		f = open("dependancy_graph/nodes_"+chars, "w")
		f.write(str(depSeg.genereNodes())) 
		f.close()

		f = open("dependancy_graph/edges_"+chars, "w")
		f.write(str(depSeg.genereEdges()))
		f.close()

		f = open("dependancy_graph/correspond", "a+")
		f.write(chars+" : "+sentence+"\n")
		f.close()
