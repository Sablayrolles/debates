#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module Test of my_spacy
# Author : SABLAYROLLES Louis
# Date : 07 / 05 / 17

# run test over the my_spacy module

import spacy_mod

"""
	Module Test-NLP
	===============
	
	This module can be use to do module test on the module my_spacy
	
"""

sp = spacy_mod.Spacy()

text = (u"Secretary Clinton and others, politicians, should have been doing this for years, not right now, because of the fact that we've created a movement. They should have been doing this for years. What's happened to our jobs and our country and our economy generally is -- look, we owe $20 trillion. We cannot do it any longer, Lester.")

sp.analyse(text)
print("Entities:")
print(sp.getEntities())
print("\nTokens:")
print(sp.tokens())
print("\nDependancy:")
sp.outputDependancy()
print("\nSentiment:")
sp.getSentiment()
