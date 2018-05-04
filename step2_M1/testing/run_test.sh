#!/bin/sh

if [ -z $1 ]; then
	echo "Usage : $0 fic_of_sentences"
	exit -1;
fi

while read ligne
do
	echo "python3 parseNLP.py \""$ligne"\""
	python3 parseNLP.py "$ligne"
done < $1
