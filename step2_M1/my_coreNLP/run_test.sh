#!/bin/sh

# Module Test of my_coreNLP
# Author : SABLAYROLLES Louis
# Date : 07 / 05 / 17

# run test over the my_coreNLP module

#on test l'usage
if [ -z $1 ]; then
	echo "Usage : $0 fic_of_sentences"
	exit -1;
fi

#on parcours le fichier de phrases et on lance le test sur chaque phrase
while read ligne
do
	echo "python test_NLP.py \""$ligne"\""
	python3 parseNLP.py "$ligne"
done < $1