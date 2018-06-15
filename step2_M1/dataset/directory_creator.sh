#!/bin/bash

echo "Usage : $0 -[h|c|y|d] (name) (year)"
echo -e "\t -h : affiche l'aide et quitte"
echo -e "\t -c : creer le pays 'name'"
echo -e "\t -y : ajoute l'annee 'year' pour le pays 'name'"
echo -e "\t -d : ajoute un debat dans le pays 'name' pour l'annee 'year'"

if [ -z $1 ]; then
	echo "not enough parameters"
	exit 1
fi;
if [ -z $2 ] && [ $1 != "-h" ]; then
	echo "name parameter require"
	exit 2
fi;
if [ -z $2 ] && [ $1 == "-h" ]; then
	exit 0;
fi;
if [ $1 != "-c" ] && [ $1 != "-y" ] && [ $1 != "-d" ]; then
	echo "$1 parameter invalide"
	exit 3
fi;

if [ $1 == "-c" ]; then
	if [ -d ./$2 ]; then
		echo "$name country already exist"
		exit 4
	else
		mkdir ./$2
		echo "$2 country create"
	fi;
fi;

if [ $1 == "-y" ]; then
	if [ -z $3 ]; then
		echo "year parameter required"
		exit 5
	fi;
	if [ ! -d ./$2 ]; then
		echo "$name country don't exist"
		exit 6
	else
		if [ -d ./$2/$3 ]; then
			echo "$2 year already exist"
			exit 7
		else
			mkdir ./$2/$3
			echo "$3 year create for $2 country"
		fi;
	fi;
fi;

if [ $1 == "-d" ]; then
	if [ -z $3 ]; then
		echo "year parameter required"
		exit 8
	fi;
	if [ ! -d ./$2 ]; then
		echo "$2 country don't exist"
		exit 9
	fi;
	if [ ! -d ./$2/$3 ]; then
		echo "$3 year for $2 country don't exist"
		exit 10
	fi
			
	name_rep=1
	while [ -d ./$2/$3/$name_rep ]; do
		let "name_rep=$name_rep+1"
	done;
	mkdir ./$2/$3/$name_rep
	mkdir ./$2/$3/$name_rep/brut/
	mkdir ./$2/$3/$name_rep/segmented/
	mkdir ./$2/$3/$name_rep/full/
	mkdir ./$2/$3/$name_rep/reactions/
	mkdir ./$2/$3/$name_rep/annotated/
	echo "./$2/$3/$name_rep arborescence create"
fi;

exit 0