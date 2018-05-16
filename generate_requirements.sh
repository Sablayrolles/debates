#!/bin/sh

# Generator of requirements file
# Author : SABLAYROLLES Louis
# Date : 09 / 05 / 17

# generate the requirements.txt file
# use pip install -r requirements.txt to install all dependancy

#pip freeze >requirements.txt

pipreqs ./step2_M1 --force #work better based on imports