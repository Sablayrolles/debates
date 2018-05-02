#!/usr/bin/python

import os
import sys

from constantes import *

#Traitements des parametres
if len(sys.argv) < MIN_ARGS+1 or len(sys.argv) > MAX_ARGS+1:
	if not MUTE:
		print "Error no enough args"
	sys.exit(NOT_ENOUGH_ARGS)
if len(sys.argv) < MIN_ARGS+2:
	if sys.argv[1] == "-h" or sys.argv[1]  == "--help":
		aff_help()
		sys.exit(0)
	else:
		PATH_CORPUS=sys.argv[1] #chemin du corpus
		hand=True
		script=True
else:
	if sys.argv[1] == "-h" or sys.argv[1]  == "--help":
		aff_help()
		sys.exit(0)
	else:
		test_more_letter=False
		if "-" not in sys.argv[1]:
			if not MUTE:
				print "First option don't contain '-'"
			sys.exit(NOT_TIRET)
		if "H" in sys.argv[1] and "S" in sys.argv[1]:
			if not MUTE:
				print "Option -H and -S incompatible"
			sys.exit(INCOMPATIBLE_ARGS)
		if "H" in sys.argv[1]:
			hand=True
			script=False
			test_more_letter=True
		if "m" in sys.argv[1]:
			MUTE=True
		if "L" in sys.argv[1]:
			LAMBDA=float(sys.argv[1][sys.argv[1].find("L")+1:sys.argv[1].find("L")+NB_CARAC_LAMBDA+1])
			test_more_letter=True
		if "M" in sys.argv[1]:
			NUM_METHOD=int(sys.argv[1][sys.argv[1].find("M")+1:sys.argv[1].find("M")+NB_CARAC_METHOD_NUM+1])
			test_more_letter=True
		if "S" in sys.argv[1]:
			script=True
			hand=False
			test_more_letter=True
		if "c" in sys.argv[1]:
			SHOW_CONTRIBUTION=True
		if "f" in sys.argv[1]:
			if not os.path.exists("./function.py"):
				if not MUTE:
					print "Fichier function.py not found"
				sys.exit(FIC_FUNCTION_NOT_FOUND)
			else:
				from function import *
			test_more_letter=True
		
		if not test_more_letter and "type=" in sys.argv[1]: 
			if "script" not in sys.argv[1] and "hand" not in sys.argv[1]:
				if not MUTE:
					print "Unknow value for option --type"
				sys.exit(UNKNOW_VALUE)
			if "script" in sys.argv[1]:
				hand=False
				script=True
			else:
				hand=True
				script=False
			test_more_letter=True
		if not test_more_letter:
			if not MUTE:
				print "Unknow option ", sys.argv[1]
			sys.exit(UNKNOW_OPTION)
		PATH_CORPUS=sys.argv[2]	
		
#Verification des chemins
name_fic=PATH_CORPUS+"NAMES.txt"
if not os.path.exists(PATH_CORPUS):
	if not MUTE:
		print "Le repertoire", PATH_CORPUS, "est introuvable"
	sys.exit(NOT_FOUND_DIRECTORY)
	
if not os.path.isdir(PATH_CORPUS):
	if not MUTE:
		print "Le repertoire", PATH_CORPUS, "n'est pas un dossier."
	sys.exit(INVALID_DIRECTORY)
	
PATH_CORPUS=PATH_CORPUS+"output/ac-aa/"
if not os.path.isdir(PATH_CORPUS):
	if not MUTE:
		print "Le corpus situe", PATH_CORPUS, "n'a pas ete traite"
	sys.exit(NOT_TREATED_DIRECTORY)


if not os.path.exists(name_fic):
	if not MUTE:
		print "Le corpus situe", PATH_CORPUS, "ne contient pas de nom"
	sys.exit(NO_NAMES)
else:
	f = open(name_fic, 'r')
	NOM_DES_CANDIDATS = f.read().split()
	
if hand:
	listFic1=[ os.path.join(PATH_CORPUS, f) for f in os.listdir(PATH_CORPUS) if os.path.isfile(os.path.join(PATH_CORPUS, f)) and "-hand_parsed.aa" in f and "autosav" not in f ]
else:
	listFic1=[]
	
if script:
	listFic2=[ os.path.join(PATH_CORPUS, f) for f in os.listdir(PATH_CORPUS) if os.path.isfile(os.path.join(PATH_CORPUS, f)) and "-scripted_parsed.aa" in f and "autosav" not in f ]
else:
	listFic2=[]
	
listFic=listFic1+listFic2
if listFic == []:
	if not MUTE:
		print "Not found .aa files"
	sys.exit(NOT_FOUND_FILES)
	
print "Param set L:"+str(LAMBDA)+", M:"+str(NUM_METHOD)