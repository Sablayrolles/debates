#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module features/creat_aam_as_files.py
# Author : SABLAYROLLES Louis
# Date : 11 / 06 / 17

# return infos of a debates

import sys
sys.path.append("./")


try:
	from . import getInfos as getInfos
except ImportError:
	import getInfos as getInfos

def combinaison(tab):
	c = []
	for e in tab:
		t = tab
		t.remove(e)
		for e2 in t:
			c.append([e,e2])
		
	return c

dir = input("directory of infos.xml (end it with /) : ")
try:
	fn=open(dir+"infos.xml","U")
	fn.close()
	infos = getInfos.getInfosDebates(dir+"infos.xml")
	
	pers = []
	pers.append(infos["presentator"])
	for n in infos["candidates"]:
		pers.append(n)
		
	combi = [", ".join(c) for c in combinaison(pers.copy())]
	combi.extend(pers)
	
	print("creating debates.aam")
	f = open(dir+"annotated/debate.aam", "w")
	f.write("<?xml version='1.0' encoding='utf-8'?>\n")
	f.write('<annotationModel>'+"\n")
	f.write('	<units>'+"\n")
	f.write('		<type groups="Bargaining_block" name="Turn">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Identifier">'+"\n")
	f.write('					<value default="" type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="Emitter">'+"\n")
	f.write('					<value default="" type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('		<type groups="Complex_discourse_unit" name="Segment" />'+"\n")
	f.write('		<type groups="Complex_discourse_unit" name="Proposition">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Surface_act">'+"\n")
	f.write('					<possibleValues default="Please choose...">'+"\n")
	f.write('						<value>Assertion</value>'+"\n")
	f.write('						<value>Question</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="recipient">'+"\n")
	f.write('					<possibleValues default="?">'+"\n")
	f.write('						<value>All</value>'+"\n")
	f.write('						<value>?</value>'+"\n")
	for p in combi:
		f.write('						<value>'+p+'</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="emitter">'+"\n")
	f.write('					<possibleValues default="Please choose...">'+"\n")
	f.write('						<value>?</value>'+"\n")
	for p in pers:
		f.write('						<value>'+p+'</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="reaction_public">'+"\n")
	f.write('					<possibleValues default="0">'+"\n")
	f.write('						<value>+</value>'+"\n")
	f.write('						<value>0</value>'+"\n")
	f.write('						<value>-</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="reaction_emitter">'+"\n")
	f.write('					<possibleValues default="0">'+"\n")
	f.write('						<value>+</value>'+"\n")
	f.write('						<value>0</value>'+"\n")
	f.write('						<value>-</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="reaction_recipient">'+"\n")
	f.write('					<possibleValues default="0">'+"\n")
	f.write('						<value>+</value>'+"\n")
	f.write('						<value>0</value>'+"\n")
	f.write('						<value>-</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('		<type groups="Complex_discourse_unit" name="Attack">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Surface_act">'+"\n")
	f.write('					<possibleValues default="Please choose...">'+"\n")
	f.write('						<value>Assertion</value>'+"\n")
	f.write('						<value>Question</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="recipient">'+"\n")
	f.write('					<possibleValues default="?">'+"\n")
	f.write('						<value>All</value>'+"\n")
	f.write('						<value>?</value>'+"\n")
	for p in combi:
		f.write('						<value>'+p+'</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="emitter">'+"\n")
	f.write('					<possibleValues default="Please choose...">'+"\n")
	f.write('						<value>?</value>'+"\n")
	for p in pers:
		f.write('						<value>'+p+'</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="reaction_public">'+"\n")
	f.write('					<possibleValues default="0">'+"\n")
	f.write('						<value>+</value>'+"\n")
	f.write('						<value>0</value>'+"\n")
	f.write('						<value>-</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="reaction_emitter">'+"\n")
	f.write('					<possibleValues default="0">'+"\n")
	f.write('						<value>+</value>'+"\n")
	f.write('						<value>0</value>'+"\n")
	f.write('						<value>-</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="reaction_recipient">'+"\n")
	f.write('					<possibleValues default="0">'+"\n")
	f.write('						<value>+</value>'+"\n")
	f.write('						<value>0</value>'+"\n")
	f.write('						<value>-</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('		<type groups="Complex_discourse_unit" name="Counterattack">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Surface_act" default="Please choose...">'+"\n")
	f.write('					<possibleValues>'+"\n")
	f.write('						<value>Assertion</value>'+"\n")
	f.write('						<value>Question</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="recipient">'+"\n")
	f.write('					<possibleValues default="?">'+"\n")
	f.write('						<value>All</value>'+"\n")
	f.write('						<value>?</value>'+"\n")
	for p in combi:
		f.write('						<value>'+p+'</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="emitter">'+"\n")
	f.write('					<possibleValues default="Please choose...">'+"\n")
	f.write('						<value>?</value>'+"\n")
	for p in pers:
		f.write('						<value>'+p+'</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="reaction_public">'+"\n")
	f.write('					<possibleValues default="0">'+"\n")
	f.write('						<value>+</value>'+"\n")
	f.write('						<value>0</value>'+"\n")
	f.write('						<value>-</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="reaction_emitter">'+"\n")
	f.write('					<possibleValues default="0">'+"\n")
	f.write('						<value>+</value>'+"\n")
	f.write('						<value>0</value>'+"\n")
	f.write('						<value>-</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="reaction_recipient">'+"\n")
	f.write('					<possibleValues default="0">'+"\n")
	f.write('						<value>+</value>'+"\n")
	f.write('						<value>0</value>'+"\n")
	f.write('						<value>-</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('		<type groups="Complex_discourse_unit" name="Question">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Surface_act">'+"\n")
	f.write('					<possibleValues default="Question">'+"\n")
	f.write('						<value>Assertion</value>'+"\n")
	f.write('						<value>Question</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="recipient">'+"\n")
	f.write('					<possibleValues default="?">'+"\n")
	f.write('						<value>All</value>'+"\n")
	f.write('						<value>?</value>'+"\n")
	for p in combi:
		f.write('						<value>'+p+'</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="emitter">'+"\n")
	f.write('					<possibleValues default="Please choose...">'+"\n")
	f.write('						<value>?</value>'+"\n")
	for p in pers:
		f.write('						<value>'+p+'</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="reaction_public">'+"\n")
	f.write('					<possibleValues default="0">'+"\n")
	f.write('						<value>+</value>'+"\n")
	f.write('						<value>0</value>'+"\n")
	f.write('						<value>-</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="reaction_emitter">'+"\n")
	f.write('					<possibleValues default="0">'+"\n")
	f.write('						<value>+</value>'+"\n")
	f.write('						<value>0</value>'+"\n")
	f.write('						<value>-</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="reaction_recipient">'+"\n")
	f.write('					<possibleValues default="0">'+"\n")
	f.write('						<value>+</value>'+"\n")
	f.write('						<value>0</value>'+"\n")
	f.write('						<value>-</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('		<type groups="Complex_discourse_unit" name="Change_of_subject">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Surface_act">'+"\n")
	f.write('					<possibleValues default="Please choose...">'+"\n")
	f.write('						<value>Assertion</value>'+"\n")
	f.write('						<value>Question</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="emitter">'+"\n")
	f.write('					<possibleValues default="Please choose...">'+"\n")
	f.write('						<value>?</value>'+"\n")
	for p in pers:
		f.write('						<value>'+p+'</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('		<type groups="Complex_discourse_unit" name="Taking_part">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Surface_act">'+"\n")
	f.write('					<possibleValues default="Please choose...">'+"\n")
	f.write('						<value>Assertion</value>'+"\n")
	f.write('						<value>Question</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="recipient">'+"\n")
	f.write('					<possibleValues default="?">'+"\n")
	f.write('						<value>All</value>'+"\n")
	f.write('						<value>?</value>'+"\n")
	for p in combi:
		f.write('						<value>'+p+'</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="emitter">'+"\n")
	f.write('					<possibleValues default="Please choose...">'+"\n")
	f.write('						<value>?</value>'+"\n")
	for p in pers:
		f.write('						<value>'+p+'</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('		<type groups="Complex_discourse_unit" name="Claim">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Surface_act">'+"\n")
	f.write('					<possibleValues default="Please choose...">'+"\n")
	f.write('						<value>Assertion</value>'+"\n")
	f.write('						<value>Question</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="emitter">'+"\n")
	f.write('					<possibleValues default="Please choose...">'+"\n")
	f.write('						<value>?</value>'+"\n")
	for p in pers:
		f.write('						<value>'+p+'</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('		<type groups="Complex_discourse_unit" name="Support">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Surface_act">'+"\n")
	f.write('					<possibleValues default="Please choose...">'+"\n")
	f.write('						<value>Assertion</value>'+"\n")
	f.write('						<value>Question</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="emitter">'+"\n")
	f.write('					<possibleValues default="Please choose...">'+"\n")
	f.write('						<value>?</value>'+"\n")
	for p in pers:
		f.write('						<value>'+p+'</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('		<type groups="Complex_discourse_unit" name="Other">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Surface_act">'+"\n")
	f.write('					<possibleValues default="Please choose...">'+"\n")
	f.write('						<value>Assertion</value>'+"\n")
	f.write('						<value>Question</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="emitter">'+"\n")
	f.write('					<possibleValues default="Please choose...">'+"\n")
	f.write('						<value>?</value>'+"\n")
	for p in pers:
		f.write('						<value>'+p+'</value>'+"\n")
	f.write('					</possibleValues>'+"\n")
	f.write('				</feature>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('	</units>'+"\n")
	f.write('	<relations>'+"\n")
	f.write('		<type groups="Discourse" name="Attack" oriented="true">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('		<type groups="Discourse" name="Avoidance" oriented="true">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('		<type groups="Discourse" name="Conditional" oriented="true">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('		<type groups="Discourse" name="Continuation" oriented="true">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('		<type groups="Discourse" name="Elaboration" oriented="true">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('		<type groups="Discourse" name="Explanation" oriented="true">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('		<type groups="Discourse" name="Q-Elab" oriented="true">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('		<type groups="Discourse" name="Q-clar" oriented="true">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('		<type groups="Discourse" name="Question-answer_pair" oriented="true">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('		<type groups="Discourse" name="Result" oriented="true">'+"\n")
	f.write('			<featureSet>'+"\n")
	f.write('				<feature name="Comments">'+"\n")
	f.write('					<value default="Please write in remarks..." type="free" />'+"\n")
	f.write('				</feature>'+"\n")
	f.write('			</featureSet>'+"\n")
	f.write('		</type>'+"\n")
	f.write('	</relations>'+"\n")
	f.write('	<schemas>'+"\n")
	f.write('		<type groups="Blocks" name="Bargaining_block">'+"\n")
	f.write('			<featureSet />'+"\n")
	f.write('		</type>'+"\n")
	f.write('		<type groups="CDUs" name="Complex_discourse_unit">'+"\n")
	f.write('			<featureSet />'+"\n")
	f.write('		</type>'+"\n")
	f.write('	</schemas>'+"\n")
	f.write('</annotationModel>'+"\n")

	f.close()
	print("debates.aam created")
	
	print("creating debates.as")
	f = open(dir+"/annotated/debate.as", "w")
	f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>'+"\n")
	f.write('<annodis-styles>'+"\n")
	f.write('<unit-style>'+"\n")
	f.write('<type name="Attack"/>'+"\n")
	f.write('<background-color b="0" g="0" r="255"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('</unit-style>'+"\n")
	f.write('<unit-style>'+"\n")
	f.write('<type name="Change_of_subject"/>'+"\n")
	f.write('<background-color b="255" g="0" r="0"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('</unit-style>'+"\n")
	f.write('<unit-style>'+"\n")
	f.write('<type name="Claim"/>'+"\n")
	f.write('<background-color b="0" g="102" r="255"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('</unit-style>'+"\n")
	f.write('<unit-style>'+"\n")
	f.write('<type name="Counterattack"/>'+"\n")
	f.write('<background-color b="0" g="0" r="51"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('</unit-style>'+"\n")
	f.write('<unit-style>'+"\n")
	f.write('<type name="Other"/>'+"\n")
	f.write('<background-color b="0" g="255" r="255"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('</unit-style>'+"\n")
	f.write('<unit-style>'+"\n")
	f.write('<type name="Proposition"/>'+"\n")
	f.write('<background-color b="0" g="255" r="0"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('</unit-style>'+"\n")
	f.write('<unit-style>'+"\n")
	f.write('<type name="Question"/>'+"\n")
	f.write('<background-color b="255" g="255" r="0"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('</unit-style>'+"\n")
	f.write('<unit-style>'+"\n")
	f.write('<type name="Support"/>'+"\n")
	f.write('<background-color b="0" g="102" r="0"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('</unit-style>'+"\n")
	f.write('<unit-style>'+"\n")
	f.write('<type name="Taking_part"/>'+"\n")
	f.write('<background-color b="204" g="0" r="102"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('</unit-style>'+"\n")
	f.write('<relation-style>'+"\n")
	f.write('<type name="Attack"/>'+"\n")
	f.write('<line-color b="0" g="0" r="204"/>'+"\n")
	f.write('<background-color b="0" g="0" r="255"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('</relation-style>'+"\n")
	f.write('<relation-style>'+"\n")
	f.write('<type name="Avoidance"/>'+"\n")
	f.write('<line-color b="153" g="0" r="153"/>'+"\n")
	f.write('<background-color b="0" g="0" r="255"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('</relation-style>'+"\n")
	f.write('<relation-style>'+"\n")
	f.write('<type name="Conditional"/>'+"\n")
	f.write('<line-color b="0" g="51" r="255"/>'+"\n")
	f.write('<background-color b="0" g="0" r="255"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('</relation-style>'+"\n")
	f.write('<relation-style>'+"\n")
	f.write('<type name="Continuation"/>'+"\n")
	f.write('<line-color b="51" g="153" r="0"/>'+"\n")
	f.write('<background-color b="0" g="0" r="255"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('</relation-style>'+"\n")
	f.write('<relation-style>'+"\n")
	f.write('<type name="Elaboration"/>'+"\n")
	f.write('<line-color b="0" g="255" r="0"/>'+"\n")
	f.write('<background-color b="0" g="0" r="255"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('</relation-style>'+"\n")
	f.write('<relation-style>'+"\n")
	f.write('<type name="Explanation"/>'+"\n")
	f.write('<line-color b="51" g="255" r="0"/>'+"\n")
	f.write('<background-color b="0" g="0" r="255"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('</relation-style>'+"\n")
	f.write('<relation-style>'+"\n")
	f.write('<type name="Q-Elab"/>'+"\n")
	f.write('<line-color b="255" g="102" r="0"/>'+"\n")
	f.write('<background-color b="0" g="0" r="255"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('</relation-style>'+"\n")
	f.write('<relation-style>'+"\n")
	f.write('<type name="Q-clar"/>'+"\n")
	f.write('<line-color b="204" g="0" r="0"/>'+"\n")
	f.write('<background-color b="0" g="0" r="255"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('</relation-style>'+"\n")
	f.write('<relation-style>'+"\n")
	f.write('<type name="Question-answer_pair"/>'+"\n")
	f.write('<line-color b="255" g="51" r="51"/>'+"\n")
	f.write('<background-color b="0" g="204" r="153"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('</relation-style>'+"\n")
	f.write('<relation-style>'+"\n")
	f.write('<type name="Result"/>'+"\n")
	f.write('<line-color b="255" g="0" r="102"/>'+"\n")
	f.write('<background-color b="0" g="0" r="255"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('</relation-style>'+"\n")
	f.write('<schema-style>'+"\n")
	f.write('<type name="Bargaining_block"/>'+"\n")
	f.write('<line-color b="0" g="0" r="153"/>'+"\n")
	f.write('<background-color b="0" g="0" r="255"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('<display-type value="barycenter-left"/>'+"\n")
	f.write('</schema-style>'+"\n")
	f.write('<schema-style>'+"\n")
	f.write('<type name="Complex_discourse_unit"/>'+"\n")
	f.write('<line-color b="75" g="0" r="125"/>'+"\n")
	f.write('<background-color b="0" g="0" r="255"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('<display-type value="barycenter-right"/>'+"\n")
	f.write('</schema-style>'+"\n")
	f.write('<schema-style>'+"\n")
	f.write('<type name="Several_resources"/>'+"\n")
	f.write('<line-color b="0" g="180" r="0"/>'+"\n")
	f.write('<background-color b="0" g="180" r="0"/>'+"\n")
	f.write('<invisibility value="false"/>'+"\n")
	f.write('<display-type value="barycenter"/>'+"\n")
	f.write('</schema-style>'+"\n")
	f.write('</annodis-styles>'+"\n")
	f.close()
	
	print("debates.as created")
except IOError: 
	print("Error: File does not appear to exist.")