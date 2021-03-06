#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module dataset/getData
# Author : SABLAYROLLES Louis
# Date : 07 / 05 / 17

# declaration of getData module to iterate on dataset files


import re

"""
	Module getData
	==============
	
	This module can be use to iterate on a data file
	
"""

class Sentences():
	"""
		Class Sentences
		===============
		
		Use it to create a iterator object.
		
		def __init__(self, fichier, entete_to_split, type="Sentences") : instanciation of iterator
		def __iter__(self) : return the current iteration 
		def next(self) : calculate and return the next iteration
		def __next__(self) : calculate and return the next iteration
	"""
	cur_ligne = -1
	n = 0
	def __init__(self, fichier, entete_to_split, numq, type="Sentences", nbE=0):
		"""
			def __init__(self, fichier, entete_to_split, numq, type="Sentences", nbE=0)
			--------------------------------------------------------------
			
			instanciation of iterator object
			
			:param fichier: nom du fichier a iterer
			:param entete_to_split: regex contenant l'entete a enlever
			:param numq: numero de la question du débat en train d'être traitée (1 par fichier normalement)
			:param type: "Sentences(blocs sur une ligne)" || "EDU(&)"
			:param nbE: numero d'EDU à partir duquel commencer
			:type fichier: string 
			:type entete_to_split: string
			:type type: string
			:type nbE: int
		"""
		fic = open(fichier,"r")
		f = fic.readlines()
		fic.close()
		
		if nbE > 0:
			self.n = nbE
		
		self.f = []
		for l in f:
			if l.strip() != "":
				m = re.search(entete_to_split, l)
				if m == None:
					print("entete:",entete_to_split,"\nlig:",l)
				
				if type == "EDU":
					for edu in re.sub(entete_to_split, '', l).split("&"):
						self.n += 1
						emmiter = m.group(0)
						d = {"num":self.n, "emmiter": emmiter, "question": numq, "edu": edu}
						if edu != '\n' and edu != '':
							self.f.append(d)
						else:
							self.n -= 1
							
				else:
					self.n += 1
					emmiter = m.group(0)
					d = {"num":self.n, "emmiter": emmiter, "question": numq, "sentences": re.sub(entete_to_split, '', l).replace("&", "").replace("\n", "")}
					self.f.append(d)
	
	def nbEDU(self):
		return self.n
					
	def __iter__(self):
		"""
			def __iter__(self)
			------------------
			
			return the iteration of sentences
			
			:return: the sentence afer the cursor in the file
			:rtype: string
		"""
		return self
	
	def next(self):
		"""
			def next(self)
			--------------
			
			calculate and return the nexte iteration
			
			:return: the next sentence afer the cursor in the file
			:rtype: string
		"""
		self.cur_ligne += 1
		
		if self.cur_ligne >= len(self.f):
			raise StopIteration
		
		return self.f[self.cur_ligne]
		
	def __next__(self):
		"""
			def __next__(self)
			------------------
			
			calculate and return the nexte iteration
			
			:return: the next sentence afer the cursor in the file
			:rtype: string
		"""
		return self.next()
		
if __name__ == "__main__":
	file = "./usa/2016/1/segmented/1.txt"
	
	for s in Sentences(file, "(^[A-Z]+: )"):
		print(s)
		a = input()