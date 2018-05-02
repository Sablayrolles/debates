#!/usr/bin/python

#Example utilisation : ./scripts/notations/evaluate_note_v1.py -HM1 ./usa/2016/1/
from constantes import *
from functions import *
from calculate import *

from verif import *
	
#data: listFic, NOM_DES_CANDIDATS

if hand:
	tt={}
	for i in NOM_DES_CANDIDATS:
		tt[i] = 0
	if not MUTE:
		print " *** Demarrage traitement fichier parse a la main *** "
	numT=0
	for fic in listFic1:
		numT += 1
		res, error, error_rate, scores = trait_fic(PATH_CORPUS, fic, NOM_DES_CANDIDATS, numT, NUM_METHOD, LAMBDA)
		if not MUTE:
			print " Traitement de "+os.path.basename(fic)+" ->", scores, "with ", error_rate, "of error rate (", error, ")"
		
		tt = pondere_q_debate_interest(numT, tt, scores, NOM_DES_CANDIDATS)
	if not MUTE:
		print "Scores finaux : ", tt
	else:
		print tt
	if not MUTE:
		print " *** Fin traitement fichier parse a la main *** "
	
if not MUTE:
	print "\n"

if script:
	tt={}
	for i in NOM_DES_CANDIDATS:
		tt[i] = 0
	if not MUTE:
		print " *** Demarrage traitement fichier parse avec le script *** "
	numT=0
	for fic in listFic2:
		numT += 1
		res, error, error_rate, scores = trait_fic(PATH_CORPUS, fic, NOM_DES_CANDIDATS, numT, NUM_METHOD, LAMBDA)
		if not MUTE:
			print " Traitement de "+os.path.basename(fic)+" ->", scores, "with ", error_rate, "of error rate (", error, ")"
		tt = pondere_q_debate_interest(numT, tt, scores, NOM_DES_CANDIDATS)
	if not MUTE:
		print "Scores finaux : ", tt
	else:
		print tt
	if not MUTE:
		print " *** Fin traitement fichier parse avec le script *** "
