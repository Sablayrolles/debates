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
import joblib
import argparse

#constantes for learning

parser = argparse.ArgumentParser(description="\tModule computeFeatures\n\t===============\n\n\t\tThis module can be use to compute and save features on a savedata computing on dataset")

parser.add_argument("numFiles", metavar="nbFiles", type=int, help="Number of file .features to learn (from computeFeatures)")
parser.add_argument("-v", "--verbose", metavar="verbose", type=int, choices=[1, 2], nargs="?", help="Level of verbose\n 0: None, 1: min (default), 2 : all")
parser.add_argument("-t", "--test", metavar="testSize", type=float, nargs="?", help="Test size between 0 and 1")
parser.add_argument("--iterMin", metavar="iterMin", type=int, nargs="?", help="Number of min iter")
parser.add_argument("--iterMax", metavar="iterMax", type=int, nargs="?", help="Number of max iter")

args = parser.parse_args()

NB_FILES = int(args.numFiles) + 1
	
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
f_dic = []
f = []
print("[Info] Loading features["+str(NB_FILES)+"] ...")
d={}
for i in range(1,int(NB_FILES)):
	data = joblib.load("../features/data/"+str(i)+".features")
	keys = []
	for k in sorted(data.keys()):
		if k != "edu" and k != "num":
			keys.append(k)
			d[k] = data[k]
	features.append(data)
	f.append([1,2,3])
print("[Data] Features keys:", keys)

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
max_scr = 0
for MAX_ITER in range(MAX_ITER_MIN,MAX_ITER_MAX):
	if VERBOSE == "min":
		print('\033[1A'+"[Info][Model=Crf][MAX_ITER="+str(MAX_ITER)+"] Learning test :", round(float(MAX_ITER-MAX_ITER_MIN) / float(MAX_ITER_MAX-MAX_ITER_MIN) * 100.0, 2),"%")
	if VERBOSE == "full":
		print("[Info][Model=Crf][MAX_ITER="+str(MAX_ITER)+"]================= NB ITER :", MAX_ITER, "======================================")
	#on split le dataset
	# features_train, features_valid, target_train, target_valid = modelSelect.train_test_split(features, targets_trans, test_size=TEST_PERCENT)
	sss = modelSelect.StratifiedShuffleSplit(n_splits=2, test_size=TEST_PERCENT)
	features_train, features_valid, target_train, target_valid = [], [], [], []
	for train_i, test_i in sss.split(f, targets):
		for i in train_i:
			features_train.append(features[i])
			target_train.append(targets[i])
	
		for i in test_i:
			features_valid.append(features[i])
			target_valid.append(targets[i])

	model = crfs.CRF(algorithm='lbfgs', c1=0.1, c2=0.1, max_iterations=MAX_ITER, all_possible_transitions=True)

	if VERBOSE == "full":
		print("[Info][Model=Classes][MAX_ITER="+str(MAX_ITER)+"] Learning...")
	
	print(len(features_train), len(target_train), set(target_train))
	model = model.fit(features_train, target_train)
		
	if VERBOSE == "full":
		print("[Info][Model=Classes][MAX_ITER="+str(MAX_ITER)+"] Testing")

	labels = list(model.classes_)
	y_pred = model.predict(features_valid)
	v = crfs.metrics.flat_accuracy_suite(y_pred, target_valid, average='weighted', labels=labels)
	if v > max_scr:
		max_scr = v
		iter_max = MAX_ITER
	if VERBOSE == "full":
		print("[Info][Model=Classes][MAX_ITER="+str(MAX_ITER)+"] Mean valid accuracy:",v)
	
print("[Info][Model=Classes] Best accuracy for", iter_max, "iteration with valid accuracy of", max_scr)
# a = input("Press Enter to Continue ...")

MAX_ITER = iter_max
print("[Valid] ================= NB ITER :", MAX_ITER, "======================================")
# features_train, features_valid, target_train, target_valid = modelSelect.train_test_split(features, targets, test_size=TEST_PERCENT)
sss = modelSelect.StratifiedShuffleSplit(n_splits=2, test_size=TEST_PERCENT)
features_train, features_valid, target_train, target_valid = [], [], [], []
for train_i, test_i in sss.split(f, targets):
	for i in train_i:
		features_train.append(features[i])
		target_train.append(targets[i])
	
	for i in test_i:
		features_valid.append(features[i])
		target_valid.append(targets[i])

print("Train composition : ")
for k in set(target_train):
	print(le.inverse_transform(k), target_train.count(k))
	
print("Valid composition : ")
for k in set(target_valid):
	print(le.inverse_transform(k), target_valid.count(k))

model = crfs.CRF(algorithm='lbfgs', c1=0.1, c2=0.1, max_iterations=MAX_ITER, all_possible_transitions=True)

print("[Valid] Learning...")
model = model.fit(features_train, target_train)

#save the model
print("[Saving] saving model")
joblib.dump(model, "modelCRF.save")
#loaded_model = joblib.load("model.save")

print("[Valid] Testing")

print("[Valid] Mean train accuracy:",model.score(features_train, target_train))
print("[Valid] Mean valid accuracy:",model.score(features_valid, target_valid))
print("[Valid] Types:", list(model.classes_))

y_pred = model.predict(features_valid)
y_pred_all = model.predict(features)

try:
	print("------------------------------")
	print("[Valid] On valid test")
	print(crfs.metrics.flat_classification_report(target_valid, y_pred, target_names=le.classes_))
	# print("[Valid] Confusion valid test")
	# print(metrics.confusion_matrix(target_valid, y_pred, labels=le.classes_))
	print("[Valid] On all corpus")
	print(crfs.metrics.classification_report(targets, y_pred_all, target_names=le.classes_))
	# print("[Valid] Confusion all corpus")
	# print(metrics.confusion_matrix(targets, y_pred_all, labels=le.classes_))
except UndefinedMetricWarning:
	pass

f = open("res", "w")

f.write("[Valid] Testing")

f.write("[Valid] Mean train accuracy:"+str(model.score(features_train, target_train)))
f.write("[Valid] Mean valid accuracy:"+str(model.score(features_valid, target_valid)))
f.write("[Valid] Types:"+ str(list(model.classes_)))

try:
	f.write("------------------------------")
	f.write("[Valid] On valid test")
	f.write(str(crfs.metrics.flat_classification_report(target_valid, y_pred, target_names=le.classes_)))
	# f.write("[Valid] Confusion valid test")
	# f.write(metrics.confusion_matrix(target_valid, y_pred, labels=le.classes_))
	f.write("[Valid] On all corpus")
	f.write(str(crfs.metrics.classification_report(targets, y_pred_all, target_names=le.classes_)))
	# print("[Valid] Confusion all corpus")
	# print(metrics.confusion_matrix(targets, y_pred_all, labels=le.classes_))
except UndefinedMetricWarning:
	pass
f.close()
