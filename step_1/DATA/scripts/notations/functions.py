#!/usr/bin/python

from constantes import *
from calculate import *

#definition des fonctions
def aff_help():
	print "Usage : "+sys.argv[0]+" -[H|S|h|-help|-type={script|hand}|Mx|Lx|c] PATH_CORPUS "
	print "\n"
	print "\n -m : mute (ne garde que le scores finaux)"
	print "\t -H : ne traite que les fichiers parse a la main (incompatible -S)"
	print "\t -S : ne traite que les fichiers parse par le script (incompatible -H)"
	print "\t    (default with no option : traite tout les fichiers .aa du repertoire"
	print "\t -Mx : utilise la methode x pour calculer les scores"
	print "\t -Lx : utiliser le lambda x pour calculer les scores"
	print "\n"
	print "\t -h | --help : affiche l'aide"
	print "\n"
	print "\t -c : affiche les contributions des lambdas dans le fichier contrib.txt"
	print "\n"
	print "\t PATH_CORPUS : chemin d'acces au corpus (contenant le repertoire output/ sinon executer ./prepare.sh)"
	print "\n"
		
def test_fic(num, lig):
	if num == 1 and ("<?xml" not in lig or "version=\"1.0\"" not in lig or "?>" not in lig):
		return False, "Ceci n'est pas un fichier xml"
	else:
		return True, ""
		
def is_EDU(lig):
	return "<unit" in lig
def nb_EDU_tt(fic):
	f=open(fic)
	ligs = f.readlines()
	f.close()
	
	num=0
	for lig in ligs:
		if is_EDU(lig):
			num += 1
	return num	
def majEDUnum(lig, num, data, test):
	if is_EDU(lig):
		num += 1
		data = {}
		test["continue"] = True
	return num, data, test
def all_test_lig(lig, previous_test):
	test={}
	test["in_EDU"] = ((is_EDU(lig) or previous_test["in_EDU"]) and "/unit" not in lig)
	test["in_metadata"] = (("metadata" in lig or previous_test["in_metadata"]) and "/metadata" not in lig)
	test["in_characterisation"] = (("characterisation" in lig or previous_test["in_characterisation"]) and "/characterisation" not in lig) 
	test["in_featureSet"] = (("featureSet" in lig or previous_test["in_featureSet"]) and "/featureSet" not in lig) 
	test["trait_type_OK"] = test["in_characterisation"] and not test["in_featureSet"] and "type" in lig
	test["trait_feature_OK"] = test["in_characterisation"] and test["in_featureSet"] and "feature" in lig
	test["compute"] = "/featureSet" in lig
	test["continue"] = previous_test["continue"]
	
	return test

def get_type(lig):
	return lig.split("type>")[1].split("</")[0]
	
def parseFeature(lig):
	try:
		lig.split("feature")[1].replace(" ", "_").split("=")[1].replace("\">"," ")[1:-2].split()
	except IndexError:
		return "", []
	else:
		return lig.split("feature")[1].replace(" ", "_").split("=")[1].replace("\">"," ")[1:-2].split()
	
def trait_fic(path, fic, names, numT, numM, LAMBDA):
	#recuperation content
	f = open(fic)
	ligs = f.readlines()
	f.close()
	
	res=True
	scores={}
	for n in names:
		scores[n] = 0
	
	lig_num_false=""
	error=""
	ignored="Line feature ignored : "
	tt_EDU=nb_EDU_tt(fic)
	
	num=0
	nb_false=0
	EDU_num=0
	data={}
	test = {"in_EDU": False, "in_metadata": False, "in_characterisation": False, "in_featureSet": False,  "trait_type_OK": False, "trait_feature_OK": False, "compute": False, "continue": True}
	
	for lig in ligs:
		lig = lig.replace("Please choose...", "Please_choose...").replace("\n","")
		num += 1;
		
		#verification type du fichier
		res, error = test_fic(num, lig)
		if not res:
			break
			
		EDU_num, data, test = majEDUnum(lig, EDU_num, data, test)
		test = all_test_lig(lig, test)
		
		#recuperation et traitement du type
		if test["trait_type_OK"] and not test["trait_feature_OK"] and test["continue"]:
			type = get_type(lig)
			if type not in TYP_TO_MATCH:
				test["continue"] = False
			
		#recuperation et traitement des features
		if test["trait_feature_OK"] and test["continue"]:
			name, value = parseFeature(lig)
			if name != "":
				data[name]=value
				
		#calcul des scores
		if test["compute"]:
			if 'Surface_act' not in data.keys():
				nb_false += 1
				lig_num_false += " " +str(num)
				res=False
				error=nb_false, "ending feature incorrectes on ligs :", lig_num_false
			else:
				if data["Surface_act"] not in SURFACE_ACT_TO_MATCH:
					ignored += str(num)+" "
				else:
					if "emitter" in data and data.get("emitter","") != "Please_choose..." and data.get("emitter","") in scores:
						scores[data.get("emitter","")] += calc_score_emitter(numM, LAMBDA, numT, EDU_num, tt_EDU, type, data.get("Surface_act",""), data.get("reaction_emitter",""), data.get("reaction_recipient",""), data.get("reaction_public",""))
					if "recipient" in data and data.get("recipient","") != "Please_choose..." and data.get("recipient","") in scores:
						scores[data.get("recipient","")] += calc_score_recipiant(numM, LAMBDA, numT, EDU_num, tt_EDU, type, data.get("Surface_act",""), data.get("reaction_emitter",""), data.get("reaction_recipient",""), data.get("reaction_public",""))
			data = {}
	return res, str(error)+str(ignored), nb_false/num*100, scores