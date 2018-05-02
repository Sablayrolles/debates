#!/usr/bin/python

from time import *

#definition des constantes
TYP_TO_MATCH=["Proposition", "Attack", "Counterattack"]
SURFACE_ACT_TO_MATCH=["Question","Assertion"]
MIN_ARGS=1
MAX_ARGS=2
NUM_METHOD=0
LAMBDA=0.90
NB_CARAC_METHOD_NUM=1
NB_CARAC_LAMBDA=4
MUTE=False
hand=True
script=True
SHOW_CONTRIBUTION=True
CONTRIB=""

#definition des erreurs
NOT_ENOUGH_ARGS=1
UNKNOW_OPTION=2
UNKNOW_VALUE=3
NOT_TIRET=4
INCOMPATIBLE_ARGS=5
FIC_FUNCTION_NOT_FOUND=6
NOT_FOUND_DIRECTORY=7
INVALID_DIRECTORY=8
NOT_TREATED_DIRECTORY=9
NOT_FOUND_FILES=10
NO_NAMES=11
