#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module emoLex/emoLex.py
# Author : SABLAYROLLES Louis
# Date : 25 / 06 / 17

# define emoLex object

import pandas

class EmoLex:
	def __init__(self, file="./english_EmoLex.csv"):
		self.f = file
		self.df = 0
		
	def load(self):
		print("[EmoLex] Loading file", self.f)
		self.df = pandas.read_csv(self.f, sep=";")
		self.df.set_index('word', inplace=True)
		self.df.sort_index(inplace=True)
		print("[EmoLex] File", self.f, "loaded")
	
	def selectCols(self, cols):
		print("[EmoLex] Selecting cols", cols)
		for col in list(set(list(self.df)).difference(set(cols))):
			self.df.drop(columns=[col], inplace=True)
			
	def getVals(self, word, col):
		try:
			return self.df.loc[word,col]
		except KeyError:
			return 0
		
if __name__ == "__main__":
	el = EmoLex()
	el.load()
	el.selectCols(["positive", "negative"])
	print(el.getVals("abovementioned", "positive"), el.getVals("abovementioned", "negative"))
	print(el.getVals("abrasion", "positive"), el.getVals("abrasion", "negative"))