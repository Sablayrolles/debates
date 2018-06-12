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
		f.append(data[k])
	del f["edu"]
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
#on trandfVsdfvgdfsg,lkrzpqfjdsmlk,fpsqdkjgform le nom des classes en nombre
le = preprocess.LabelEncoder()
le = le.fit(types)
targets_trans = le.transform(targets)
	
#on split le dataset
features_train, features_valid, target_train, target_valid = modelSelect.train_test_split(features, targets_trans, test_size=0.33)

model = linear_model.LogisticRegression(solver='saga', max_iter=MAX_ITER, multi_class='ovr', n_jobs=NB_CORE)
#multi_class = 'ovr' ==> regression binaire sur chaque label /='multinomial' sinon
#solver = For multiclass problems, only ‘newton-cg’, ‘sag’, ‘saga’ and ‘lbfgs’

print("Learning...")
model = model.fit(features_train, target_train)
print("Testing")
print("Mean accuracy:",model.score(features_valid, target_valid))
