#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Module features/computeFeatures.py
# Author : SABLAYROLLES Louis
# Date : 11 / 06 / 17

# compute features

import joblib

for n in range(1,730):
	print("EDU num : ",n)
	
	data = joblib.load("./data/"+str(n)+".data")
	print(data)
	
	a=input()