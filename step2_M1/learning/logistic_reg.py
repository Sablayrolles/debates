#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module features/wordFeatures.py
# Author : SABLAYROLLES Louis
# Date : 11 / 06 / 17

# learn over features

import sys
sys.path.append("..")
import dataset.parse_types_annoted as getTarget

import sklearn.model_selection as modelSelect
import sklearn.linear_model as linear_model
import sklearn.preprocessing as preprocess
import sklearn.metrics as metrics
import joblib

#constantes for learning
NB_CORE = 16 
MAX_ITER_MIN = 100
MAX_ITER_MAX = 1000
TEST_PERCENT = 0.1
VERBOSE = "min"

if len(sys.argv) != 2:
	print("Usage ", sys.argv[0]," nbFeaturesFiles")
	sys.exit(1)

print("[Param] NB_CORE :", NB_CORE)
print("[Param] MAX_ITER_MIN :", MAX_ITER_MIN)
print("[Param] MAX_ITER_MAX :", MAX_ITER_MAX)
print("[Param] TEST_PERCENT :", TEST_PERCENT)
print("[Param] VERBOSE :", VERBOSE)

### recupération des données
features = []
f_dic = []
print("[Info] Loading features...")
for i in range(1,int(sys.argv[1])):
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
	# features_train, features_valid, target_train, target_valid = modelSelect.train_test_split(features, targets_trans, test_size=TEST_PERCENT)
	sss = modelSelect.StratifiedShuffleSplit(n_splits=2, test_size=TEST_PERCENT)
	features_train, features_valid, target_train, target_valid = [], [], [], []
	for train_i, test_i in sss.split(features, targets_trans):
		for i in train_i:
			features_train.append(features[i])
			target_train.append(targets_trans[i])
	
		for i in test_i:
			features_valid.append(features[i])
			target_valid.append(targets_trans[i])

	model = linear_model.LogisticRegression(solver='sag', max_iter=MAX_ITER, multi_class='multinomial', n_jobs=NB_CORE)
	#multi_class = 'ovr' ==> regression binaire sur chaque label /='multinomial' sinon
	#solver = For multiclass problems, only ‘newton-cg’, ‘sag’, ‘saga’ and ‘lbfgs’

	if VERBOSE == "full":
		print("[Info][Model=Classes][MAX_ITER="+str(MAX_ITER)+"] Learning...")
	model = model.fit(features_train, target_train)
	if VERBOSE == "full":
		print("[Info][Model=Classes][MAX_ITER="+str(MAX_ITER)+"] Testing")

	if VERBOSE == "full":
		print("[Info][Model=Classes][MAX_ITER="+str(MAX_ITER)+"] Mean train accuracy:",model.score(features_train, target_train))
	v = model.score(features_valid, target_valid)
	if v > max_scr:
		max_scr = v
		iter_max = MAX_ITER
	if VERBOSE == "full":
		print("[Info][Model=Classes][MAX_ITER="+str(MAX_ITER)+"] Mean valid accuracy:",v)
	
print("[Info][Model=Classes] Best accuracy for", iter_max, "iteration with valid accuracy of", max_scr)
# a = input("Press Enter to Continue ...")

MAX_ITER = iter_max
print("[Valid] ================= NB ITER :", MAX_ITER, "======================================")
# features_train, features_valid, target_train, target_valid = modelSelect.train_test_split(features, targets_trans, test_size=TEST_PERCENT)
sss = modelSelect.StratifiedShuffleSplit(n_splits=2, test_size=TEST_PERCENT)
features_train, features_valid, target_train, target_valid = [], [], [], []
for train_i, test_i in sss.split(features, targets_trans):
	for i in train_i:
		features_train.append(features[i])
		target_train.append(targets_trans[i])
	
	for i in test_i:
		features_valid.append(features[i])
		target_valid.append(targets_trans[i])

print("Train composition : ")
for k in set(target_train):
	print(k, target_train.count(k))
	
print("Valid composition : ")
for k in set(target_valid):
	print(k, target_valid.count(k))

model = linear_model.LogisticRegression(solver='lbfgs', max_iter=MAX_ITER, multi_class='multinomial', n_jobs=NB_CORE)
#multi_class = 'ovr' ==> regression binaire sur chaque label /='multinomial' sinon
#solver = For multiclass problems, only ‘newton-cg’, ‘sag’, ‘saga’ and ‘lbfgs’

print("[Valid] Learning...")
model = model.fit(features_train, target_train)

#save the model
print("[Saving] saving model")
joblib.dump(model, "model.save")
#loaded_model = joblib.load("model.save")

print("[Valid] Testing")

print("[Valid] Mean train accuracy:",model.score(features_train, target_train))
print("[Valid] Mean valid accuracy:",model.score(features_valid, target_valid))
print("[Valid] Types:", le.inverse_transform(model.classes_))
print("[Valid] weights:", model.coef_)

y_pred = model.predict(features_valid)
y_pred_all = model.predict(features)

print("------------------------------")
print("[Valid] On valid test")
print(metrics.classification_report(target_valid, y_pred, target_names=le.classes_))
print("[Valid] On all corpus")
print(metrics.classification_report(targets_trans, y_pred_all, target_names=le.classes_))
