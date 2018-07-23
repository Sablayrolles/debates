#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module learning/xrf.py
# Author : SABLAYROLLES Louis
# Date : 11 / 06 / 17

# learn over features with conditional random field

import sys
sys.path.append("..")

import sklearn.model_selection as modelSelect
import sklearn.preprocessing as preprocess
import sklearn.metrics as metrics
import sklearn_crfsuite as crfs
import sklearn_crfsuite.metrics as crfsMetrics
import joblib
import argparse
import pickle

#constantes for learning

parser = argparse.ArgumentParser(description="\tModule computeFeatures\n\t===============\n\n\t\tThis module can be use to compute and save features on a savedata computing on dataset")

parser.add_argument("numFiles", metavar="nbFiles", type=int, help="Number of file .features to learn (from computeFeatures)")
parser.add_argument("-c", "--core", metavar="core", type=int, nargs="?", help="Nb core to execute (default 1)")
parser.add_argument("-v", "--verbose", metavar="verbose", type=int, choices=[0, 1, 2], nargs="?", help="Level of verbose\n 0: None, 1: min (default), 2 : all")
parser.add_argument("-t", "--test", metavar="testSize", type=float, nargs="?", help="Test size between 0 and 1")
parser.add_argument("--iterMin", metavar="iterMin", type=int, nargs="?", help="Number of min iter")
parser.add_argument("--iterMax", metavar="iterMax", type=int, nargs="?", help="Number of max iter")

args = parser.parse_args()

NB_FILES = int(args.numFiles) + 1

if args.core != None:
	NB_CORE = int(args.core)
else:
	NB_CORE = 1
		
if args.test != None:
	if float(args.test) > 0.0 and float(args.test) < 1.0:
		TEST_PERCENT = float(args.test)
	else:
		sys.stderr.write("Test percent need to be between 0.0 and 1.0")
		sys.exit(-2)
else:
	TEST_PERCENT = 0.1
	
if args.iterMin != None:
	MAX_ITER_MIN = int(args.iterMin)
else:
	MAX_ITER_MIN = 100
	
if args.iterMax != None:
	MAX_ITER_MAX = int(args.iterMax)
else:
	MAX_ITER_MAX = 1000
	
if args.verbose != None:
	if args.verbose == 0:
		VERBOSE = ""
	if args.verbose == 1:
		VERBOSE = "min"
	if args.verbose == 2:
		VERBOSE = "full"
else:
	VERBOSE = "min"

print("[Param] NB_FILES :", NB_FILES)
print("[Param] MAX_ITER_MIN :", MAX_ITER_MIN)
print("[Param] MAX_ITER_MAX :", MAX_ITER_MAX)
print("[Param] TEST_PERCENT :", TEST_PERCENT)
print("[Param] VERBOSE :", VERBOSE)

### recupération des données
features = []
f = []
keys = []
print("[Info] Loading features["+str(NB_FILES)+"] ...")
for i in range(1,int(NB_FILES)):
	data = joblib.load("../features/data/"+str(i)+".features")
	features.append(data)
	d = []
	#on fait une matrice il n'aime pas les dics
	for k in sorted(data.keys()):
		if k != "edu" and k != "num":
			if k not in keys:
				keys.append(k)
			d.append(data[k])
	f.append(d)
print("[Data] Features keys("+str(len(keys))+") : ", keys)

print("[Info] Loading targets...")
d = joblib.load("../features/data/targets.dat")
targets_full = d["data"]
targets = []
for i in features:
	if (i["question"],i["edu"]) not in targets_full.keys():
		targets.append("Other")
	else:
		#auto replace for low cat
		if targets_full[(i["question"],i["edu"])] == "Change_of_subject":
			targets.append("Proposition")
		if targets_full[(i["question"],i["edu"])] == "Taking_part":
			targets.append("Support")
		
		if targets_full[(i["question"],i["edu"])] not in ["Change_of_subject", "Taking_part"]:
			targets.append(targets_full[(i["question"],i["edu"])])
			
print("[Data] Targets Types classifier : ", set(targets))
for k in set(targets):
	print(k, targets.count(k))
print("[Info] Number examples (Classes):", len(features), "and", len(targets), "of targets.")

### LEARNING CLASSES
# a = input("Press Enter to Continue ...")
print("[Info] Learning Classes...\n")
iter_max = 0
c1_max = 0
c2_max = 0
max_scr = 0
first = True

def train(c1, c2, MAX_ITER):
	global targets
	global features
	global MAX_ITER_MAX
	global MAX_ITER_MIN
	global VERBOSE
	global TEST_PERCENT
	global first
	
	print("("+str(c1)+","+str(c2)+","+str(MAX_ITER)+")")
	if VERBOSE == "min":
		print('\033[1A'+"[Info][Model=Crf][MAX_ITER="+str(MAX_ITER)+"] Learning test :", round(float(MAX_ITER-MAX_ITER_MIN) / float(MAX_ITER_MAX-MAX_ITER_MIN) * 100.0, 2),"%")
	if VERBOSE == "full":
		print("[Info][Model=Crf][MAX_ITER="+str(MAX_ITER)+"]================= NB ITER :", MAX_ITER, "======================================")
	#on split le dataset
	# features_train, features_test, target_train, target_test = modelSelect.train_test_split(features, targets_trans, test_size=TEST_PERCENT)
	sss = modelSelect.StratifiedShuffleSplit(n_splits=2, test_size=TEST_PERCENT)
	features_train, features_test, target_train, target_test = [], [], [], []
	for train_i, test_i in sss.split(f, targets):
		for i in train_i:
			features_train.append(features[i])
			target_train.append(targets[i])
	
		for i in test_i:
			features_test.append(features[i])
			target_test.append(targets[i])

	model = crfs.CRF(algorithm='lbfgs', c1=c1, c2=c2, max_iterations=MAX_ITER, all_possible_transitions=True)

	if VERBOSE == "full":
		print("[Info][Model=Classes][MAX_ITER="+str(MAX_ITER)+"] Learning...")
	
	# print(len(features_train), len(target_train), set(target_train))
	model = model.fit([features_train], [target_train])
		
	if VERBOSE == "full":
		print("[Info][Model=Classes][MAX_ITER="+str(MAX_ITER)+"] Testing")

	labels = list(model.classes_)
	y_pred = model.predict([features_test])
	v = crfsMetrics.flat_accuracy_score(y_pred, [target_test])
	if first:
		scrs = []
		first = False
	else:
		scrs = joblib.load("/home/lsablayr/stageM1/debates/step2_M1/learning/scrs")
	scrs.append([c1,c2,MAX_ITER,v])
	joblib.dump(scrs, "scrs", pickle.HIGHEST_PROTOCOL, compress=True)
	del scrs
	if v > max_scr:
		max_scr = v
		iter_max = MAX_ITER
		c1_max = c1
		c2_max = c2
		joblib.dump(model, "modelCRF.save")
		print("New best accuracy for crf model with c1 =", c1, "c2 =", c2, "MAX_ITER =", MAX_ITER, "score :", v)
	if VERBOSE == "full":
		print("[Info][Model=Classes][MAX_ITER="+str(MAX_ITER)+"] Mean test accuracy:",v)
				
				
def paraWork(c1):
	for c2 in [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]:
		print("For c1 =", c1, "c2 =", c2)
		for MAX_ITER in range(MAX_ITER_MIN,MAX_ITER_MAX):
			train(c1, c2, MAX_ITER)
			
if NB_CORE == 1:
	for c1 in [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]:
		paraWork(c1)
else:
	joblib.Parallel(n_jobs=NB_CORE,verbose=5,backend="multiprocessing")(joblib.delayed(paraWork)(c1) for c1 in [0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]) 
"""
print("[Info][Model=Classes] Best accuracy for", iter_max, "iterations and c1 =", c1, "and c2 =", c2, " with test accuracy of", max_scr)
# a = input("Press Enter to Continue ...")

MAX_ITER = iter_max
print("[test] ================= NB ITER :", MAX_ITER, "======================================")
# features_train, features_test, target_train, target_test = modelSelect.train_test_split(features, targets, test_size=TEST_PERCENT)
sss = modelSelect.StratifiedShuffleSplit(n_splits=2, test_size=TEST_PERCENT)
features_train, features_test, target_train, target_test = [], [], [], []
for train_i, test_i in sss.split(f, targets):
	for i in train_i:
		features_train.append(features[i])
		target_train.append(targets[i])
	
	for i in test_i:
		features_test.append(features[i])
		target_test.append(targets[i])

print("Train composition : ")
for k in set(target_train):
	print(k, target_train.count(k))
	
print("test composition : ")
for k in set(target_test):
	print(k, target_test.count(k))

# model = crfs.CRF(algorithm='lbfgs', c1=0.1, c2=0.1, max_iterations=MAX_ITER, all_possible_transitions=True)

# print("[test] Learning...")
# model = model.fit([features_train], [target_train])

#save the model
print("[Load] Loading best model")
model = joblib.load("model.save")

print("[test] Testing")

print("[test] Mean train accuracy:",model.score([features_train], [target_train]))
print("[test] Mean test accuracy:",model.score([features_test], [target_test]))
print("[test] Types:", list(model.classes_))

y_pred = model.predict([features_test])
y_pred_all = model.predict([features])

try:
	print("------------------------------")
	print("[test] On test test")
	print(crfsMetrics.flat_classification_report([target_test], y_pred, target_names=list(model.classes_)))
	# print("[test] Confusion test test")
	# print(metrics.confusion_matrix(target_test, y_pred, labels=le.classes_))
	print("[test] On all corpus")
	print(crfsMetrics.classification_report([targets], y_pred_all, target_names=list(model.classes_)))
	# print("[test] Confusion all corpus")
	# print(metrics.confusion_matrix(targets, y_pred_all, labels=le.classes_))
except UndefinedMetricWarning:
	pass

f = open("res", "w")

f.write("[test] Testing")

f.write("[test] Mean train accuracy:"+str(model.score([features_train], [target_train])))
f.write("[test] Mean test accuracy:"+str(model.score([features_test], [target_test])))
f.write("[test] Types:"+ str(list(model.classes_)))

try:
	f.write("------------------------------")
	f.write("[test] On test test")
	f.write(str(crfsMetrics.flat_classification_report([target_test], y_pred, target_names=list(model.classes_))))
	# f.write("[test] Confusion test test")
	# f.write(metrics.confusion_matrix(target_test, y_pred, labels=le.classes_))
	f.write("[test] On all corpus")
	f.write(str(crfsMetrics.classification_report([targets], y_pred_all, target_names=list(model.classes_))))
	# print("[test] Confusion all corpus")
	# print(metrics.confusion_matrix(targets, y_pred_all, labels=le.classes_))
except UndefinedMetricWarning:
	pass
f.close()
"""