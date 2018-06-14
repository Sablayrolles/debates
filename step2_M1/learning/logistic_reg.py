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
TEST_PERCENT = 0.33
VERBOSE = False

print("[Param] NB_CORE :", NB_CORE)
print("[Param] MAX_ITER_MIN :", MAX_ITER_MIN)
print("[Param] MAX_ITER_MAX :", MAX_ITER_MAX)
print("[Param] TEST_PERCENT :", TEST_PERCENT)
print("[Param] VERBOSE :", VERBOSE)

#recupération des données
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
		targets.append("ToDetermine")
	else:
		targets.append(targets_full[(i["question"],i["edu"])])
		
### Split ToDetermine / others
featuresToDet = []
targetsToDet = []
featuresTypes = []
targetsTypes = []
toDetType = []
typesType = []
for f, t in zip(features, targets):
	if t == "ToDetermine":
		if t not in toDetType:
			toDetType.append(t)
		featuresToDet.append(f)
		targetsToDet.append(t)
	else:
		if "NotToDetermine" not in toDetType:
			toDetType.append("NotToDetermine")
		if t not in typesType:
			typesType.append(t)
		featuresToDet.append(f)
		targetsToDet.append("NotToDetermine")
		featuresTypes.append(f)
		targetsTypes.append(t)
print("[Data] Targets ToDetermine classifier : ", toDetType)
print("[Data] Targets Types classifier : ", typesType)
a = input("Press Enter to Continue ...")

print("[Info] Preprocessing...")
#on transform le nom des classes en nombre
le_to_det = preprocess.LabelEncoder()
le_to_det = le_to_det.fit(toDetType)
targetsToDet_trans = le_to_det.transform(targetsToDet)

le_classes = preprocess.LabelEncoder()
le_classes = le_classes.fit(typesType)
targetsTypes_trans = le_classes.transform(targetsTypes)

print("[Info] Number examples (To determine):", len(featuresToDet))
print("[Info] Number examples (Classes):", len(featuresTypes))
a = input("Press Enter to Continue ...")	

print("[Info] Learning To determine")
iter_max = 0
max_scr = 0
for MAX_ITER in range(MAX_ITER_MIN,MAX_ITER_MAX):
	print("Learning test :", float(MAX_ITER) / float(MAX_ITER_MAX-MAX_ITER_MIN) * 100.0,"%")
	if VERBOSE:
		print("================= NB ITER :", MAX_ITER, "======================================")
	#on split le dataset
	features_train, features_valid, target_train, target_valid = modelSelect.train_test_split(featuresToDet, targetsToDet_trans, test_size=TEST_PERCENT)

	model = linear_model.LogisticRegression(solver='sag', max_iter=MAX_ITER, multi_class='multinomial', n_jobs=NB_CORE)
	#multi_class = 'ovr' ==> regression binaire sur chaque label /='multinomial' sinon
	#solver = For multiclass problems, only ‘newton-cg’, ‘sag’, ‘saga’ and ‘lbfgs’

	if VERBOSE:
		print("[Info][Model=Todetermine][MAX_ITER="+str(MAX_ITER)+"] Learning...")
	model = model.fit(features_train, target_train)
	if VERBOSE:
		print("[Info][Model=Todetermine][MAX_ITER="+str(MAX_ITER)+"]Testing")

	if VERBOSE:
		print("[Info][Model=Todetermine][MAX_ITER="+str(MAX_ITER)+"]Mean train accuracy:",model.score(features_train, target_train))
		print("[Info][Model=Todetermine][MAX_ITER="+str(MAX_ITER)+"]Mean valid accuracy:",model.score(features_valid, target_valid))
	v = model.score(features_valid, target_valid)
	if v > max_scr:
		max_scr = v
		iter_max = MAX_ITER
	if VERBOSE:
		print("[Info][Model=Todetermine][MAX_ITER="+str(MAX_ITER)+"]Mean valid accuracy:",v)
	
print("[Info][Model=Todetermine][MAX_ITER="+str(MAX_ITER)+"]Best accuracy for", iter_max, "iteration with valid accuracy of", max_scr)
a = input("Press Enter to Continue ...")

"""
MAX_ITER = iter_max
print("================= NB ITER :", MAX_ITER, "======================================")
features_train, features_valid, target_train, target_valid = modelSelect.train_test_split(features, targets_trans, test_size=0.33)

model = linear_model.LogisticRegression(solver='sag', max_iter=MAX_ITER, multi_class='multinomial', n_jobs=NB_CORE)
#multi_class = 'ovr' ==> regression binaire sur chaque label /='multinomial' sinon
#solver = For multiclass problems, only ‘newton-cg’, ‘sag’, ‘saga’ and ‘lbfgs’

print("Learning...")
model = model.fit(features_train, target_train)
print("Testing")

print("Mean train accuracy:",model.score(features_train, target_train))
print("Mean valid accuracy:",model.score(features_valid, target_valid))
print("Types:", le.inverse_transform(model.classes_))
print("weights:", model.coef_)


y_pred = model.predict(features_valid)
y_pred_all = model.predict(features)
print("y_pred:", le.inverse_transform(y_pred))
print("y_target:", le.inverse_transform(target_valid))

print("------------------------------")
print("On valid test")
print(metrics.classification_report(target_valid, y_pred, target_names=le.classes_))
print("On all corpus")
print(metrics.classification_report(targets_trans, y_pred_all, target_names=le.classes_))
"""
