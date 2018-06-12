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
import joblib

#constantes for learning
NB_CORE = 4
MAX_ITER = 100

#recupération des données
features = []
f_dic = []
print("Loading features...")
for i in range(1,730):
	data = joblib.load("../features/data/"+str(i)+".features")
	f_dic.append(data)
	f = []
	#on fait une matrice il n'aime pas les dics
	for k in sorted(data.keys()):
		if k != "edu":
			f.append(data[k])
	features.append(f)

print("Loading targets...")
targets_full, types = getTarget.getTypes1stdebate("../dataset/usa/2016/1/output/ac-aa/", 9)
targets = []
for i in f_dic:
	if (i["question"],i["edu"]) not in targets_full:
		targets.append("ToDetermine")
		if "ToDetermine" not in types:
			types.append("ToDetermine")
	else:
		targets.append(targets_full[(i["question"],i["edu"])])

print("Preprocessing...")
#on transform le nom des classes en nombre
le = preprocess.LabelEncoder()
le = le.fit(types)
targets_trans = le.transform(targets)

print("Number ex:", len(features))
	
#on split le dataset

iter_max = 0
max_scr = 0
for MAX_ITER in range(100,1000):
	print("================= NB ITER :", MAX_ITER, "======================================")
	features_train, features_valid, target_train, target_valid = modelSelect.train_test_split(features, targets_trans, test_size=0.33)

	model = linear_model.LogisticRegression(solver='sag', max_iter=MAX_ITER, multi_class='multinomial', n_jobs=NB_CORE)
	#multi_class = 'ovr' ==> regression binaire sur chaque label /='multinomial' sinon
	#solver = For multiclass problems, only ‘newton-cg’, ‘sag’, ‘saga’ and ‘lbfgs’

	print("Learning...")
	model = model.fit(features_train, target_train)
	print("Testing")

	print("Mean train accuracy:",model.score(features_train, target_train))
	v = model.score(features_valid, target_valid)
	if v > max_scr:
		max_scr = v
		iter_max = MAX_ITER
	print("Mean valid accuracy:",v)
	
print("Best accuracy for", iter_max, "iteration with valid accuracy of", max_scr)
