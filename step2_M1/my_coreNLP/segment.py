#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module my_coreNLP/segment
# Author : SABLAYROLLES Louis
# Date : 09 / 05 / 17

# own class of segment parse of corenlp

import pickle
import pprint

"""
	Module segment
	===============
	
	This module can be use to segment parsing of corenlp.
	
"""

class Parser:
	def __init__(self, data):
		self.data = data
		
	
		
if __name__ == '__main__':
	data = pickle.load(open("segmentation.nlp", "rb"))
	
	my_p = Parser(data)
	