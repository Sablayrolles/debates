#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module features/wordFeatures.py
# Author : SABLAYROLLES Louis
# Date : 11 / 06 / 17

# learn over features

import sys
sys.path.append("..")
import sklearn.linear_model as linear_model

#constantes for learning
NB_CORE = 4
MAX_ITER = 100

#recupération des données

model = linear_model.LogisticRegression(solver='saga', max_iter=MAX_ITER, multi_class='ovr', n_jobs=NB_CORE)
#multi_class = 'ovr' ==> regression binaire sur chaque label /='multinomial' sinon
#solver = For multiclass problems, only ‘newton-cg’, ‘sag’, ‘saga’ and ‘lbfgs’

model.fit(features_train, target_train)
model.score(features_valid, target_valid)