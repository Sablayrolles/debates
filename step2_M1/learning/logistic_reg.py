#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module learning/logistic_reg.py
# Author : SABLAYROLLES Louis
# Date : 11 / 06 / 17

# learn over features with logistical regression

import sys
sys.path.append("..")

import sklearn.model_selection as modelSelect
import sklearn.linear_model as linear_model
import sklearn.preprocessing as preprocess
import sklearn.metrics as metrics
import joblib
import argparse

#constantes for learning

parser = argparse.ArgumentParser(description="\tModule computeFeatures\n\t===============\n\n\t\tThis module can be use to compute and save features on a savedata computing on dataset")

parser.add_argument("numFiles", metavar="nbFiles", type=int, help="Number of file .features to learn (from computeFeatures)")
parser.add_argument("-c", "--core", metavar="core", type=int, nargs="?", help="Nb core to execute (default 1)")
parser.add_argument("-v", "--verbose", metavar="verbose", type=int, choices=[1, 2], nargs="?", help="Level of verbose\n 0: None, 1: min (default), 2 : all")
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
	
print("[Param] NB_CORE :", NB_CORE)
print("[Param] NB_FILES :", NB_FILES)
print("[Param] MAX_ITER_MIN :", MAX_ITER_MIN)
print("[Param] MAX_ITER_MAX :", MAX_ITER_MAX)
print("[Param] TEST_PERCENT :", TEST_PERCENT)
print("[Param] VERBOSE :", VERBOSE)

### recupération des données
features = []
f_dic = []
print("[Info] Loading features["+str(NB_FILES)+"] ...")
for i in range(1,int(NB_FILES)):
	data = joblib.load("../features/data/"+str(i)+".features")
	f_dic.append(data)
	f = []
	#on fait une matrice il n'aime pas les dics
	keys = []
	for k in sorted(data.keys()):
		if k != "edu" and k != "num":
			keys.append(k)
			f.append(data[k])
	features.append(f)
print("[Data] Features keys:", keys)

print("[Info] Loading targets...")
d = joblib.load("../features/data/targets.dat")
targets_full = d["data"]
targets = []
for i in f_dic:
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
types = list(set(targets))
print(types)
### PRE PROCESSING
print("[Info] Preprocessing...")
#on transform le nom des classes en nombre
le = preprocess.LabelEncoder()
le = le.fit(types)
targets_trans = le.transform(targets)

print("[Info] Number examples (Classes):", len(features))

### LEARNING CLASSES
# a = input("Press Enter to Continue ...")
print("[Info] Learning Classes...\n")
iter_max = 0
max_scr = 0
for MAX_ITER in range(MAX_ITER_MIN,MAX_ITER_MAX):
	if VERBOSE == "min":
		print('\033[1A'+"[Info][Model=Classes][MAX_ITER="+str(MAX_ITER)+"] Learning test :", round(float(MAX_ITER-MAX_ITER_MIN) / float(MAX_ITER_MAX-MAX_ITER_MIN) * 100.0, 2),"%")
	if VERBOSE == "full":
		print("[Info][Model=Classes][MAX_ITER="+str(MAX_ITER)+"]================= NB ITER :", MAX_ITER, "======================================")
	#on split le dataset
	# features_train, features_test, target_train, target_test = modelSelect.train_test_split(features, targets_trans, test_size=TEST_PERCENT)
	sss = modelSelect.StratifiedShuffleSplit(n_splits=2, test_size=TEST_PERCENT)
	features_train, features_test, target_train, target_test = [], [], [], []
	for train_i, test_i in sss.split(features, targets_trans):
		for i in train_i:
			features_train.append(features[i])
			target_train.append(targets_trans[i])
	
		for i in test_i:
			features_test.append(features[i])
			target_test.append(targets_trans[i])

	model = linear_model.LogisticRegression(solver='liblinear', max_iter=MAX_ITER, multi_class='ovr', n_jobs=NB_CORE)
	#multi_class = 'ovr' ==> regression binaire sur chaque label /='multinomial' sinon
	#solver = For multiclass problems, liblinear, newton-cg, lbfgs and sag solvers,

	if VERBOSE == "full":
		print("[Info][Model=Classes][MAX_ITER="+str(MAX_ITER)+"] Learning...")
	
	try:
		model = model.fit(features_train, target_train)
	except ConvergenceWarning:
		pass
		
	if VERBOSE == "full":
		print("[Info][Model=Classes][MAX_ITER="+str(MAX_ITER)+"] Testing")

	if VERBOSE == "full":
		print("[Info][Model=Classes][MAX_ITER="+str(MAX_ITER)+"] Mean train accuracy:",model.score(features_train, target_train))
	v = model.score(features_test, target_test)
	if v > max_scr:
		max_scr = v
		iter_max = MAX_ITER
	if VERBOSE == "full":
		print("[Info][Model=Classes][MAX_ITER="+str(MAX_ITER)+"] Mean test accuracy:",v)
	
print("[Info][Model=Classes] Best accuracy for", iter_max, "iteration with test accuracy of", max_scr)
# a = input("Press Enter to Continue ...")

MAX_ITER = iter_max
print("[test] ================= NB ITER :", MAX_ITER, "======================================")
# features_train, features_test, target_train, target_test = modelSelect.train_test_split(features, targets_trans, test_size=TEST_PERCENT)
sss = modelSelect.StratifiedShuffleSplit(n_splits=2, test_size=TEST_PERCENT)
features_train, features_test, target_train, target_test = [], [], [], []
for train_i, test_i in sss.split(features, targets_trans):
	for i in train_i:
		features_train.append(features[i])
		target_train.append(targets_trans[i])
	
	for i in test_i:
		features_test.append(features[i])
		target_test.append(targets_trans[i])

print("Train composition : ")
for k in set(target_train):
	print(le.inverse_transform(k), target_train.count(k))
	
print("test composition : ")
for k in set(target_test):
	print(le.inverse_transform(k), target_test.count(k))

model = linear_model.LogisticRegression(solver='liblinear', max_iter=MAX_ITER, multi_class='ovr', n_jobs=NB_CORE)
#multi_class = 'ovr' ==> regression binaire sur chaque label /='multinomial' sinon
#solver = For multiclass problems, liblinear, newton-cg, lbfgs and sag solvers,

print("[test] Learning...")
model = model.fit(features_train, target_train)

#save the model
print("[Saving] saving model")
joblib.dump(model, "model.save")
#loaded_model = joblib.load("model.save")

print("[test] Testing")

print("[test] Mean train accuracy:",model.score(features_train, target_train))
print("[test] Mean test accuracy:",model.score(features_test, target_test))
print("[test] Types:", le.inverse_transform(model.classes_))
print("[test] weights:", model.coef_)

y_pred = model.predict(features_test)
y_pred_all = model.predict(features)

try:
	print("------------------------------")
	print("[test] On test test")
	print(metrics.classification_report(target_test, y_pred, target_names=le.classes_))
	# print("[test] Confusion test test")
	# print(metrics.confusion_matrix(target_test, y_pred, labels=le.classes_))
	print("[test] On all corpus")
	print(metrics.classification_report(targets_trans, y_pred_all, target_names=le.classes_))
	# print("[test] Confusion all corpus")
	# print(metrics.confusion_matrix(targets_trans, y_pred_all, labels=le.classes_))
except UndefinedMetricWarning:
	pass

f = open("res", "w")

f.write("[test] Testing")

f.write("[test] Mean train accuracy:"+str(model.score(features_train, target_train)))
f.write("[test] Mean test accuracy:"+str(model.score(features_test, target_test)))
f.write("[test] Types:"+ str(le.inverse_transform(model.classes_)))
f.write("[test] weights:"+ str(model.coef_))

try:
	f.write("------------------------------\n")
	f.write("[test] On test test\n")
	d = metrics.classification_report(target_test, y_pred, target_names=le.classes_)
	f.write(str(d)+"\n")
	f.write("[test] On all corpus"+"\n")
	d = metrics.classification_report(targets_trans, y_pred_all, target_names=le.classes_)
	f.write(str(d)+"\n")
	#f.write("[test] Confusion all corpus"+"\n")
	#d = metrics.confusion_matrix(targets_trans, y_pred_all, labels=le.classes_)
	#f.write(str(d)+"\n")
except UndefinedMetricWarning:
	pass
f.close()
