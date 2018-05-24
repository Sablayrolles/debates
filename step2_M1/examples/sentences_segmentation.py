#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")

import my_coreNLP.parseNLP as parseNLP

def print_tab(t):
	i = 0
	for e in t:
		print("["+str(i)+"]",e)
		i += 1

sentences = "It's a great thing for companies to expand. And when these people are going to put billions and billions of dollars into companies, and when they're going to bring $2.5 trillion back from overseas, where they can't bring the money back, because politicians like Secretary Clinton won't allow them to bring the money back, because the taxes are so onerous, and the bureaucratic red tape, so what -- is so bad. So what they're doing is they're leaving our country, and they're, believe it or not, leaving because taxes are too high and because some of them have lots of money outside of our country. And instead of bringing it back and putting the money to work, because they can't work out a deal. We have a president that can't sit them around a table and get them to approve something. And here's the thing. Republicans and Democrats agree but we have no leadership. And honestly, that starts with Secretary Clinton."
 
print("In:", sentences)
sNLP = parseNLP.StanfordNLP()
sentences_tab = sNLP.segmente(sentences) #segmentation par phrase

print("\nOut:")
print_tab(sentences_tab)
