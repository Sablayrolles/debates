#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")

import my_coreNLP.parseNLP as parseNLP

import features.saveData as saveData
import features.computeFeatures as computeFeatures

NLP = parseNLP.StanfordNLP()
txt = {"num": 1, "question": 1, "edu": "My cat is eating the mouse!"}

s = saveData.compute(txt, NLP)
f = computeFeatures.returnFeatures(s, ["as?", "as!", "nb1stPers", "nb2ndPers"])

print(f)