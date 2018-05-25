#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module tools/RappelPrecisionFMesure
# Author : SABLAYROLLES Louis
# Date : 24 / 05 / 17

# own file to evaluate Rappel, Precision and FMesure

import pprint

"""
	Module RappelPrecisionFMesure
	=============================
	
	This module can be use to evaluate Rappel, Precision and FMesure over segmented texts.
	
"""

class FScores:
	def __init__(self, type):
		self.type = type
		
		self.fscore = {}
		for t in self.type:
			self.fscore[t] = []
			
	def addScore(self, type, nbPreditsBonSegments, nbPreditFauxSegments, nbNonPreditsBonSegments):
		self.fscore[type].append({'VP':nbPreditsBonSegments, 'FP': nbPreditFauxSegments, 'FN':nbNonPreditsBonSegments})
		
	def saisieScore(self, type):
		nbPreditsBonSegments = input("Nombre de bon segments prédits : ")
		nbPreditFauxSegments = input("Nombre de mauvais segments prédits : ")
		nbNonPreditsBonSegments = input("Nombre de bon segments non prédits : ")
		
		self.addScore(type, nbPreditsBonSegments, nbPreditFauxSegments, nbNonPreditsBonSegments)
		
	def getPrecisions(self, type):
		p = []
		for i in self.fscore[type]:
			p.append(float(i['VP'])/(float(i['VP']) + float(i['FP'])))
			
		return p
		
	def getMoyPrecision(self, type):
		return sum(self.getPrecisions(type)) / (float(len(self.getPrecisions(type))))
		
	def getRappels(self, type):
		r = []
		for i in self.fscore[type]:
			r.append(float(i['VP'])/(float(i['VP']) + float(i['FN'])))
		
		return r
		
	def getMoyRappel(self, type):
		return sum(self.getRappels(type)) / (float(len(self.getRappels(type))))
		
	def getFMesures(self, type):
		f = []
		precisions = self.getPrecisions(type)
		rappels = self.getRappels(type)
		
		for p,r in zip(precisions, rappels):
			f.append(2.0*((p*r)/(p+r)))
			
		return f
		
	def getMoyFMesure(self, type):
		return sum(self.getFMesures(type)) / (float(len(self.getFMesures(type))))