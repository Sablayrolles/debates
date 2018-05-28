#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module tools/RappelPrecisionFMesure
# Author : SABLAYROLLES Louis
# Date : 28 / 05 / 17

# own file to evaluate Rappel, Precision and FMesure

import pprint

"""
	Module RappelPrecisionFMesure
	=============================
	
	This module can be use to evaluate Rappel, Precision and FMesure over segmented texts.
	
"""

class FScores:
	"""
		Class FScores
		=============
		
		Use it to manage F-Scores and measures depending
		
		def __init__(self, types) : init F-Scores over all types contains in types tabular
		def addScore(self, type, nbPreditsBonSegments, nbPreditFauxSegments, nbNonPreditsBonSegments) : add a new F-score with all the given parameters to the type type
		def saisieScore(self, type) : allow people to get the scores on the keyboard and store them
		def getPrecisions(self, type) : return all the precisions for a given type
		def getMoyPrecision(self, type) : return the mean of precision for a given type
		def getRappels(self, type) : return all the recall for a given type
		def getMoyRappel(self, type) : return the mean of recall for a given type
		def getFMesures(self, type) : return all the F-measures for a given type
		def getMoyFMesure(self, type) : return the mean of F-measures for a given type
	"""
	def __init__(self, types):
		"""
			def __init__(self, types)
			-------------------------
			
			init F-Scores over all types contains in types tabular
			
			:param types: all types to add for the measures
			:type types: string list
		"""
		self.types = types
		
		self.fscore = {}
		for t in self.types:
			self.fscore[t] = []
			
	def addScore(self, type, nbPreditsBonSegments, nbPreditFauxSegments, nbNonPreditsBonSegments):
		"""
			def addScore(self, type, nbPreditsBonSegments, nbPreditFauxSegments, nbNonPreditsBonSegments)
			---------------------------------------------------------------------------------------------
			
			add a new F-score with all the given parameters to the type type
			
			:param type: category for adding the score
			:param nbPreditsBonSegments: number of good segment predicts
			:param nbPreditFauxSegments: number of segment predicts false
			:param nbNonPreditsBonSegments: number of good segment unpredicted
			:type type: string
			:type nbPreditsBonSegments: int
			:type nbPreditFauxSegments: int
			:type nbNonPreditsBonSegments: int
		"""
		self.fscore[type].append({'VP':nbPreditsBonSegments, 'FP': nbPreditFauxSegments, 'FN':nbNonPreditsBonSegments})
		
	def saisieScore(self, type):
		"""
			def saisieScore(self, type)
			---------------------------
			
			allow people to get the scores on the keyboard and store them
			
			:param type: type of the score to get
			:type type: string list
		"""
		nbPreditsBonSegments = input("Nombre de bon segments prédits : ")
		nbPreditFauxSegments = input("Nombre de mauvais segments prédits : ")
		nbNonPreditsBonSegments = input("Nombre de bon segments non prédits : ")
		
		self.addScore(type, nbPreditsBonSegments, nbPreditFauxSegments, nbNonPreditsBonSegments)
		
	def getPrecisions(self, type):
		"""
			def getPrecisions(self, type)
			-----------------------------
			
			return all the precisions for a given type
			
			:param type: category for the precision
			:type type: string
			:return: list of all precision for a given type
			:rtype: float list
		"""
		p = []
		for i in self.fscore[type]:
			p.append(float(i['VP'])/(float(i['VP']) + float(i['FP'])))
			
		return p
		
	def getMoyPrecision(self, type):
		"""
			def getMoyPrecision(self, type)
			-------------------------------
			
			return the mean of precision for a given type
			
			:param type: category for the precision
			:type type: string
			:return: mean of all precision for a given type
			:rtype: float
		"""
		return sum(self.getPrecisions(type)) / (float(len(self.getPrecisions(type))))
		
	def getRappels(self, type):
		"""
			def getRappels(self, type)
			--------------------------
			
			return all the recall for a given type
			
			:param type: category for the recall
			:type type: string
			:return: list of all recall for a given type
			:rtype: float list
		"""
		r = []
		for i in self.fscore[type]:
			r.append(float(i['VP'])/(float(i['VP']) + float(i['FN'])))
		
		return r
		
	def getMoyRappel(self, type):
		"""
			def getMoyRappel(self, type)
			----------------------------
			
			return the mean of recall for a given type
			
			:param type: category for the recall
			:type type: string
			:return: mean of all recall for a given type
			:rtype: float
		"""
		return sum(self.getRappels(type)) / (float(len(self.getRappels(type))))
		
	def getFMesures(self, type):
		"""
			def getFMesures(self, type)
			---------------------------
			
			return all the F-measures for a given type
			
			:param type: category for the F-measures
			:type type: string
			:return: list of all F-measures for a given type
			:rtype: float list
		"""
		f = []
		precisions = self.getPrecisions(type)
		rappels = self.getRappels(type)
		
		for p,r in zip(precisions, rappels):
			f.append(2.0*((p*r)/(p+r)))
			
		return f
		
	def getMoyFMesure(self, type):
		"""
			def getMoyFMesure(self, type)
			-----------------------------
			
			return the mean of F-measures for a given type
			
			:param type: category for the F-measures
			:type type: string
			:return: mean of all F-measures for a given type
			:rtype: float
		"""
		return sum(self.getFMesures(type)) / (float(len(self.getFMesures(type))))