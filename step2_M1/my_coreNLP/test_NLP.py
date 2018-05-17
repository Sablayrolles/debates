#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module Test of my_coreNLP
# Author : SABLAYROLLES Louis
# Date : 07 / 05 / 17

# run test over the my_coreNLP module

import parseNLP

import sys
sys.path.append("..")
from counter import timer
import random
import pprint

"""
	Module Test-NLP
	===============
	
	This module can be use to do module test on the module parseNLP
	
"""

def save_to_file(name, struct):
	"""
		def save_to_file(name, struct)
		------------------------------
		
		ecrit une structure de facon lisible dans un fichier
		
		:param name: nom du fichier de sortie
		:param struct: structure a ecrire
		:type name: string 
		:type struct: ??
	"""
	f = open(name, "w")
	f.write(str(struct))
	f.close()
	
def test(sNLP, text):
	"""
		def test(sNLP, text)
		--------------------
		
		effectue l'ensemble des tests des méthodes de la classe StanfordNLP et sauvegarde les résultats
		
		:param sNLP: objet NLP
		:param text: phrase a tester
		:type sNLP: NLP object 
		:type text: string
	"""
	text = sys.argv[1]
	time = {}
	chars = "".join([random.choice(list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxytz0123456789")) for i in range(15)])

	t = timer.Timer()

	t.start()
	print("\tannotate")
	save_to_file("./fics/annotate_"+chars, sNLP.annotate(text))
	time["annotate"] = t.stop()

	t.start()
	print("\tpos")
	save_to_file("./fics/pos_"+chars, sNLP.pos(text))
	time["pos"] = t.stop()

	t.start()
	print("\ttokens")
	save_to_file("./fics/tokens_"+chars, sNLP.word_tokenize(text))
	time["tokens"] = t.stop()

	t.start()
	print("\tner")
	save_to_file("./fics/ner_"+chars, sNLP.ner(text))
	time["ner"] = t.stop()

	t.start()
	print("\tparse")
	save_to_file("./fics/parse_"+chars, sNLP.parse(text))
	time["parse"] = t.stop()

	t.start()
	print("\tdependancy")
	save_to_file("./fics/dependancy_"+chars, sNLP.dependency_parse(text))
	time["dependancy"] = t.stop()

	print("\ttimer")
	save_to_file("./fics/timer_"+chars, time)
	
	f = open("./fics/corespond_random_chain", "a+")
	f.write(chars+" : "+text+"\n")
	f.close()

if __name__ == '__main__':
	sNLP = parseNLP.StanfordNLP()

	if len(sys.argv) != 2:
		print("Usage : $0 \"phrase\"")
		
		text = u"It's a great thing for companies to expand. And when these people are going to put billions and billions of dollars into companies, and when they're going to bring $2.5 trillion back from overseas, where they can't bring the money back, because politicians like Secretary Clinton won't allow them to bring the money back, because the taxes are so onerous, and the bureaucratic red tape, so what is so bad." # So what they're doing is they're leaving our country, and they're, believe it or not, leaving because taxes are too high and because some of them have lots of money outside of our country. And instead of bringing it back and putting the money to work, because they can't work out a deal. We have a president that can't sit them around a table and get them to approve something. And here's the thing. Republicans and Democrats agree but we have no leadership. And honestly, that starts with Secretary Clinton."
		
		print("Obtain : ")
		print([" ".join(t) for t in sNLP.segmente(text)])
	else:
		test(sNLP, sys.argv[1])
