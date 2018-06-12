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
import joblib

#constantes for learning
NB_CORE = 4
MAX_ITER = 100

#recupération des données
features = []
for i in range(1,730):
	features.append(joblib.load("../features/data/"+str(i)+".features"))
targets_full = getTarget.getTypes1stdebate("../dataset/usa/2016/1/output/ac-aa/", 9)
targets = []
for i in features:
	targets.append(targets_full[(i["question"],i["edu"])])
	del i["edu"]

print(features)
a = input();
features_train, features_valid, target_train, target_valid = modelSelect.train_test_split(features, targets, test_size=0.33)


model = linear_model.LogisticRegression(solver='saga', max_iter=MAX_ITER, multi_class='ovr', n_jobs=NB_CORE)
#multi_class = 'ovr' ==> regression binaire sur chaque label /='multinomial' sinon
#solver = For multiclass problems, only ‘newton-cg’, ‘sag’, ‘saga’ and ‘lbfgs’

model.fit(features_train, target_train)
model.score(features_valid, target_valid)