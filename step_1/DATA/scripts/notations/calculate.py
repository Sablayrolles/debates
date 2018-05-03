#!/usr/bin/python

from constantes import *
	
#definition des calculs
def help_calc():
	print "\t         pondere(typeEDU, surface_Act) : associe un coefficient a chaque type d'EDU en fonction de surface_Act"
	print "\t         note(valueReact) : associe un couple [bool,int] value_connue,note a chaque valeur de reaction"
	print "\t         coeff_public(note) : associe un coeff a la note de la reaction du public"
	print "\t         scoring_topic(numEDU) : associe un coeff en fonction du numero de l'EDU"
	print "\t         interest(numTopic) : donne un coeff en fonction de l'interet de la question aborde"
	print "\t         calc_score_emitter(numTopic, EDU_num, tt_EDU, type, Surface_Act, reaction_emitter, reaction_recipiant, reaction_public) : calcul le score de l'emetteur"
	print "\t         calc_score_recipiant(numTopic, EDU_num, tt_EDU, type, Surface_Act, reaction_emitter, reaction_recipiant, reaction_public) : calcul le score du recipiant"
	print "\t         pondere_q_debate_interest(numTopic, scoresTT, scores_topic, nomcandidats) : calcul le score global depuis le debut en fonction du score precedant et de celui de la question"
	
def pondere(typeEDU, surface_Act):
	nb = 0
	if surface_Act == "Question":
		nb += -0.5
	if surface_Act == "Assertion":
		nb += 1
		
	if typeEDU == "Attack":
		nb += 2
	if typeEDU == "CounterAttack":
		nb += 4.5
	if typeEDU == "Proposition":
		nb += 1
		
	return nb
def note(valueReact):
	note={"+": 1, "-": -1, "0": 0.1, "Please_choose...": 0.1, "Please choose...": 0.1}
	
	if valueReact not in note:
		return [False,0]
	else:
		return [True,note[valueReact]]
def coeff_public(note):
	return note
def scoring_topic(numEDU):
	global LAMBDA
	return LAMBDA**numEDU
def interest(numTopic):
	return 1
def pondere_q_debate_interest(numTopic, scoresTT, scores_topic, nomcandidats):
	global NUM_METHOD
	if NUM_METHOD <4 or NUM_METHOD >7:
		for i in nomcandidats:
			if i in scores_topic.keys():
				scoresTT[i] += scores_topic[i]
	else:
		for i in nomcandidats:
			if i in scores_topic.keys():
				scoresTT[i] += scores_topic[i]*interest(numTopic)
	return scoresTT
	
def scoreE0(LAMBDA, numTopic, EDU_num, tt_EDU, type, Surface_act, reaction_emitter, reaction_recipiant, reaction_public):
	s=note(reaction_emitter)[1]+note(reaction_public)[1]
	global SHOW_CONTRIBUTION
	if SHOW_CONTRIBUTION:
		print "M0L"+str(LAMBDA)+"Qe"+str(numTopic)+"-"+str(EDU_num)+"/"+str(tt_EDU)+"\tlambda:"+str(0)+" | score:"+str(s)
	return s
def scoreE1(LAMBDA, numTopic, EDU_num, tt_EDU, type, Surface_act, reaction_emitter, reaction_recipiant, reaction_public):
	s=pondere(type, Surface_act)*note(reaction_emitter)[1]+note(reaction_public)[1]-note(reaction_recipiant)[1]
	global SHOW_CONTRIBUTION
	if SHOW_CONTRIBUTION:
		print "M1L"+str(LAMBDA)+"Qe"+str(numTopic)+"-"+str(EDU_num)+"/"+str(tt_EDU)+"\tlambda:"+str(0)+" | score:"+str(s)
	return s
def scoreE2(LAMBDA, numTopic, EDU_num, tt_EDU, type, Surface_act, reaction_emitter, reaction_recipiant, reaction_public):
	s=scoreE0(LAMBDA, numTopic, EDU_num, tt_EDU, type, Surface_act, reaction_emitter, reaction_recipiant, reaction_public)*scoring_topic(EDU_num)
	global SHOW_CONTRIBUTION
	if SHOW_CONTRIBUTION:
		print "M2L"+str(LAMBDA)+"Qe"+str(numTopic)+"-"+str(EDU_num)+"/"+str(tt_EDU)+"\tlambda:"+str(scoring_topic(EDU_num))+" | score:"+str(s)
	return s
def scoreE3(LAMBDA, numTopic, EDU_num, tt_EDU, type, Surface_act, reaction_emitter, reaction_recipiant, reaction_public):
	s=scoreE1(LAMBDA, numTopic, EDU_num, tt_EDU, type, Surface_act, reaction_emitter, reaction_recipiant, reaction_public)*scoring_topic(EDU_num)
	global SHOW_CONTRIBUTION
	if SHOW_CONTRIBUTION:
		print "M3L"+str(LAMBDA)+"Qe"+str(numTopic)+"-"+str(EDU_num)+"/"+str(tt_EDU)+"\tlambda:"+str(scoring_topic(EDU_num))+" | score:"+str(s)
	return s
def calc_score_emitter(NUM_METHOD, *arg):
	if NUM_METHOD == 0 or NUM_METHOD == 4:
		return scoreE0(*arg)
	if NUM_METHOD == 1 or NUM_METHOD == 5:
		return scoreE1(*arg)
	if NUM_METHOD == 2 or NUM_METHOD == 6:
		return scoreE2(*arg)
	if NUM_METHOD == 3 or NUM_METHOD == 7:
		return scoreE3(*arg)
	if not MUTE:
		print "Unknow NUM_METHOD"
	return 0
	
def scoreR0(LAMBDA, numTopic, EDU_num, tt_EDU, type, Surface_act, reaction_emitter, reaction_recipiant, reaction_public):
	s=note(reaction_recipiant)[1]+note(reaction_public)[1]
	global SHOW_CONTRIBUTION
	if SHOW_CONTRIBUTION:
		print "M0L"+str(LAMBDA)+"Qr"+str(numTopic)+"-"+str(EDU_num)+"/"+str(tt_EDU)+"\tlambda:"+str(0)+" | score:"+str(s)
	return s
def scoreR1(LAMBDA, numTopic, EDU_num, tt_EDU, type, Surface_act, reaction_emitter, reaction_recipiant, reaction_public):
	s=pondere(type, Surface_act)*note(reaction_recipiant)[1]+note(reaction_public)[1]-note(reaction_emitter)[1]
	global SHOW_CONTRIBUTION
	if SHOW_CONTRIBUTION:
		print "M1L"+str(LAMBDA)+"Qr"+str(numTopic)+"-"+str(EDU_num)+"/"+str(tt_EDU)+"\tlambda:"+str(0)+" | score:"+str(s)
	return s
def scoreR2(LAMBDA, numTopic, EDU_num, tt_EDU, type, Surface_act, reaction_emitter, reaction_recipiant, reaction_public):
	s=scoreR0(LAMBDA, numTopic, EDU_num, tt_EDU, type, Surface_act, reaction_emitter, reaction_recipiant, reaction_public)*scoring_topic(EDU_num)
	if SHOW_CONTRIBUTION:
		print "M2L"+str(LAMBDA)+"Qr"+str(numTopic)+"-"+str(EDU_num)+"/"+str(tt_EDU)+"\tlambda:"+str(scoring_topic(EDU_num))+" | score:"+str(s)
	return s
def scoreR3(LAMBDA, numTopic, EDU_num, tt_EDU, type, Surface_act, reaction_emitter, reaction_recipiant, reaction_public):
	s=scoreR1(LAMBDA, numTopic, EDU_num, tt_EDU, type, Surface_act, reaction_emitter, reaction_recipiant, reaction_public)*scoring_topic(EDU_num)
	if SHOW_CONTRIBUTION:
		print "M3L"+str(LAMBDA)+"Qr"+str(numTopic)+"-"+str(EDU_num)+"/"+str(tt_EDU)+"\tlambda:"+str(scoring_topic(EDU_num))+" | score:"+str(s)
	return s
def calc_score_recipiant(NUM_METHOD, *arg):
	if NUM_METHOD == 0 or NUM_METHOD == 4:
		return scoreR0(*arg)
	if NUM_METHOD == 1 or NUM_METHOD == 5:
		return scoreR1(*arg)
	if NUM_METHOD == 2 or NUM_METHOD == 6:
		return scoreR2(*arg)
	if NUM_METHOD == 3 or NUM_METHOD == 7:
		return scoreR3(*arg)
	if not MUTE:
		print "Unknow NUM_METHOD"
	return 0