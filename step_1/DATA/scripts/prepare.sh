#!/bin/bash

echo "Usage $0 path_corpus_1 ... path_corpus_n\n"
echo "ex: $0 ./usa/2016/1/"

if [ ! -f ./scripts/config/config.txt ]; then
	echo -e "Need config to prepare ....\n"
	./scripts/config/config.sh
fi;

date=`head -1 ./scripts/config/config.txt`
brut=`head -2 ./scripts/config/config.txt | tail -1 | cut -d\; -f2`
segmented=`head -3 ./scripts/config/config.txt | tail -1 | cut -d\; -f2`

echo -e "Configuration from ./scripts/config/config.txt write on the $date loaded.\n"
echo -e "\t brut rep : $brut"
echo -e "\t segmented rep : $segmented"

if [ -z $1 ]; then
	echo "no corpus to do"
	exit 0;
fi;

for i in "$@"; do
	echo $i
	if [ ${i:0:2} == "./" ]; then
		j=${i:2:${#i}-2}
		i=$j
	fi;
	echo $i
	if [ ${i:${#i}-1:1} == "/" ]; then
		j=${i:0:${#i}-1}
		i=$j
	fi;
	echo -e "Traitement du corpus located in $i \n--> "
	
	if [ ! -d $i/$brut ] || [ ! -d $i/$segmented ]; then
		echo -e "\033[31m Wrong name of directory (Nedding in $i {$brut/,$segmented/})\033[0m\n\033[1;91mAborted.\033[0m"
	else
		echo -e "\033[32m Directories founded.\033[0m"
		#-------------------------------------------------
		
		mkdir $i/data/ 2>/dev/null
		mkdir $i/data/brut 2>/dev/null
		mkdir $i/data/segmented 2>/dev/null

		mkdir $i/output 2>/dev/null
		mkdir $i/output/ac-aa 2>/dev/null
		mkdir $i/output/aam 2>/dev/null

		#corpus file :: 
		#Name: texte(pas de :)\r\n

		cp $i/$brut/* $i/data/brut
		cp $i/$segmented/* $i/data/segmented

		echo "Creating scripted parsed ac and aa --> "
		for fic in `ls $i/data/brut`; do
			name=${fic%%.*}
			cd scripts
			python ./debates_txttoglozz.py -f ../$i/data/brut/$fic
			mv .aa $name-scripted_parsed.aa
			mv .ac $name-scripted_parsed.ac
			cd ..
		done;
		echo -e "Done\n"

		echo "Creating hand parsed ac and aa --> "
		for fic in `ls $i/data/segmented`; do
			name=${fic%%.*}
			cd scripts
			python ./debates_txttoglozz.py -f ../$i/data/segmented/$fic
			mv .aa $name-hand_parsed.aa
			mv .ac $name-hand_parsed.ac
			cd ..
		done;
		echo -e "Done\n"
		
		echo "Creating script parsed aam --> "
		for fic in `ls $i/data/brut`; do
			name=${fic%%.*}
			name=${name%%.*}
			cd scripts
			python ./debates_create_glozz_aam.py ../$i/data/brut/$fic $name-scripted_parsed.aam
			cd ..
		done;
		echo -e "Done\n"
		
		echo "Creating hand parsed aam --> "
		for fic in `ls $i/data/segmented`; do
			name=${fic%%.*}
			cd scripts
			python ./debates_create_glozz_aam.py ../$i/data/brut/$fic $name-hand_parsed.aam
			cd ..
		done;
		echo -e "Done\n"
		
		rm -R $i/data

		mv ./scripts/*.aa $i/OUTPUT/ac-aa
		mv ./scripts/*.ac $i/OUTPUT/ac-aa
		mv ./scripts/*.aam $i/OUTPUT/aam
		# ------------------------------------------------
		echo -e "\033[1;92m Finished.\033[0m"
	fi;
done;