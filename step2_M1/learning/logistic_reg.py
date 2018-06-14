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

print("[Param] NB_CORE :", NB_CORE)
print("[Param] MAX_ITER_MIN :", MAX_ITER_MIN)
print("[Param] MAX_ITER_MAX :", MAX_ITER_MAX)
print("[Param] TEST_PERCENT :", TEST_PERCENT)
print("[Param] VERBOSE :", VERBOSE)

### recupération des données
features = []
f_dic = []
print("[Info] Loading features...")
for i in range(1,730):
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
targets_full, _ = getTarget.getTypes1stdebate("../dataset/usa/2016/1/output/ac-aa/", 9)
targets = []
for i in f_dic:
	if (i["question"],i["edu"]) not in targets_full.keys():
		targets.append("Other")
	else:
		targets.append(targets_full[(i["question"],i["edu"])])
		
### Split Others / types
featuresOthers = []
targetsOthers = []
featuresTypes = []
targetsTypes = []
othersType = []
typesType = []
for f, t in zip(features, targets):
	if t == "Other":
		if t not in othersType:
			othersType.append(t)
		featuresOthers.append(f)
		targetsOthers.append(t)
	else:
		if "ToDetermine" not in othersType:
			othersType.append("ToDetermine")
		if t not in typesType:
			typesType.append(t)
		featuresOthers.append(f)
		targetsOthers.append("ToDetermine")
		featuresTypes.append(f)
		targetsTypes.append(t)
print("[Data] Targets Others classifier : ", othersType)
print("[Data] Targets Types classifier : ", typesType)
# a = input("Press Enter to Continue ...")

### PRE PROCESSING
print("[Info] Preprocessing...")
#on transform le nom des classes en nombre
le_others = preprocess.LabelEncoder()
le_others = le_others.fit(othersType)
targetsToDet_trans = le_others.transform(targetsOthers)

le_classes = preprocess.LabelEncoder()
le_classes = le_classes.fit(typesType)
targetsTypes_trans = le_classes.transform(targetsTypes)

print("[Info] Number examples (To determine):", len(featuresOthers))
print("[Info] Number examples (Classes):", len(featuresTypes))
# a = input("Press Enter to Continue ...")	

### LEARNING OTHERS
print("[Info] Learning Others...\n")
iter_max = 0
max_scr = 0
for MAX_ITER in range(MAX_ITER_MIN,MAX_ITER_MAX):
	if VERBOSE == "min":
		print('\033[1A'+"[Info][Model=Others][MAX_ITER="+str(MAX_ITER)+"] Learning test :", round(float(MAX_ITER-MAX_ITER_MIN) / float(MAX_ITER_MAX-MAX_ITER_MIN) * 100.0, 2),"%")
	if VERBOSE == "full":
		print("================= NB ITER :", MAX_ITER, "======================================")
	#on split le dataset
	# features_train, features_valid, target_train, target_valid = modelSelect.train_test_split(featuresOthers, targetsToDet_trans, test_size=TEST_PERCENT)
	sss = modelSelect.StratifiedShuffleSplit(n_splits=1, test_size=TEST_PERCENT)
	train_idx, test_idx = list(sss.split(featuresOthers, targetsToDet_trans, group=targetsOthers))[0]
	features_train, features_valid, target_train, target_valid = [], [], [], []
	for i, j in zip(train_idx, test_idx):
		features_train.append(featuresOthers[i])
		features_valid.append(featuresOthers[j])
		target_train.append(targetsToDet_trans[i])
		target_valid.append(targetsToDet_trans[j])

	model = linear_model.LogisticRegression(solver='liblinear', max_iter=MAX_ITER, n_jobs=NB_CORE)
	#multi_class = 'ovr' ==> regression binaire sur chaque label /='multinomial' sinon
	#solver = For multiclass problems, only ‘newton-cg’, ‘sag’, ‘saga’ and ‘lbfgs’

	if VERBOSE == "full":
		print("[Info][Model=Others][MAX_ITER="+str(MAX_ITER)+"] Learning...")
	model = model.fit(features_train, target_train)
	if VERBOSE == "full":
		print("[Info][Model=Others][MAX_ITER="+str(MAX_ITER)+"] Testing")

	if VERBOSE == "full":
		print("[Info][Model=Others][MAX_ITER="+str(MAX_ITER)+"] Mean train accuracy:",model.score(features_train, target_train))
		print("[Info][Model=Others][MAX_ITER="+str(MAX_ITER)+"] Mean valid accuracy:",model.score(features_valid, target_valid))
	v = model.score(features_valid, target_valid)
	if v > max_scr:
		max_scr = v
		iter_max = MAX_ITER
	if VERBOSE == "full":
		print("[Info][Model=Others][MAX_ITER="+str(MAX_ITER)+"] Mean valid accuracy:",v)
	
print("[Info][Model=Others] Best accuracy for", iter_max, "iteration with valid accuracy of", max_scr)
# a = input("Press Enter to Continue ...")

MAX_ITER = iter_max
print("[Valid] ================= NB ITER :", MAX_ITER, "======================================")
# features_train, features_valid, target_train, target_valid = modelSelect.train_test_split(featuresOthers, targetsToDet_trans, test_size=TEST_PERCENT)
sss = modelSelect.StratifiedShuffleSplit(n_splits=10, test_size=TEST_PERCENT)
train_idx, test_idx = list(sss.split(featuresOthers, targetsToDet_trans, group=targetsOthers))[0]
features_train, features_valid, target_train, target_valid = [], [], [], []
for i, j in zip(train_idx, test_idx):
	features_train.append(featuresOthers[i])
	features_valid.append(featuresOthers[j])
	target_train.append(targetsToDet_trans[i])
	target_valid.append(targetsToDet_trans[j])

model = linear_model.LogisticRegression(solver='liblinear', max_iter=MAX_ITER, n_jobs=NB_CORE)
#multi_class = 'ovr' ==> regression binaire sur chaque label /='multinomial' sinon
#solver = For multiclass problems, only ‘newton-cg’, ‘sag’, ‘saga’ and ‘lbfgs’

print("[Valid] Learning...")
model = model.fit(features_train, target_train)
print("[Valid] Testing")

print("[Valid] Mean train accuracy:",model.score(features_train, target_train))
print("[Valid] Mean valid accuracy:",model.score(features_valid, target_valid))
print("[Valid] Types:", le_others.inverse_transform(model.classes_))
print("[Valid] weights:", model.coef_)

y_pred = model.predict(features_valid)
y_pred_all = model.predict(featuresOthers)

print("------------------------------")
print("[Valid] On valid test")
print(metrics.classification_report(target_valid, y_pred, target_names=le_others.classes_))
print("[Valid] On all corpus")
print(metrics.classification_report(targetsToDet_trans, y_pred_all, target_names=le_others.classes_))

"""
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
	features_train, features_valid, target_train, target_valid = modelSelect.train_test_split(featuresTypes, targetsTypes_trans, test_size=TEST_PERCENT)

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
		print("[Info][Model=Classes][MAX_ITER="+str(MAX_ITER)+"] Mean valid accuracy:",model.score(features_valid, target_valid))
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
features_train, features_valid, target_train, target_valid = modelSelect.train_test_split(featuresTypes, targetsTypes_trans, test_size=TEST_PERCENT)

model = linear_model.LogisticRegression(solver='sag', max_iter=MAX_ITER, multi_class='multinomial', n_jobs=NB_CORE)
#multi_class = 'ovr' ==> regression binaire sur chaque label /='multinomial' sinon
#solver = For multiclass problems, only ‘newton-cg’, ‘sag’, ‘saga’ and ‘lbfgs’

print("[Valid] Learning...")
model = model.fit(features_train, target_train)
print("[Valid] Testing")

print("[Valid] Mean train accuracy:",model.score(features_train, target_train))
print("[Valid] Mean valid accuracy:",model.score(features_valid, target_valid))
print("[Valid] Types:", le_classes.inverse_transform(model.classes_))
print("[Valid] weights:", model.coef_)

y_pred = model.predict(features_valid)
y_pred_all = model.predict(featuresTypes)

print("------------------------------")
print("[Valid] On valid test")
print(metrics.classification_report(target_valid, y_pred, target_names=le_classes.classes_))
print("[Valid] On all corpus")
print(metrics.classification_report(targetsTypes_trans, y_pred_all, target_names=le_classes.classes_))
"""