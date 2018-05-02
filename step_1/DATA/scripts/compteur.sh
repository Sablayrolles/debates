#!/bin/bash

if [ -z $3 ]; then
	echo -e "Usage: $0 PATH_CORPUS ENS_LETTER_CANDIDATE [name_fic_result] [tab|brut]\n\n PATH_CORPUS: chemin d'acces au corpus (tout les fichiers *.txt du dossiers seront pris en compte)\n ENS_LETTER_CANDIDATE: liste des lettres des candidats\n name_fic_result : sortie\n [tab|brut] : format de sortie un tableau ou les donnes brutes \n Results:\n"
fi;

if [ -z $1 ] || [ -z $2 ] || [ ! -d ./$1 ]; then
	echo "Wrong arguments"
	exit 1
fi

res=0;
ch1=""
ch2=""
ch3=""
tiret=""

function cpt(){
	#$1 : dossier
	#$2 : chaine
	cd $1
	x=0;
	for f in `ls`; do
		n=`grep -c "$2" $f`
		let "x=$x+$n"
	done;
	cd - >/dev/null
	res=$x
}

function adapt(){
	l1=${#1}
	l2=${#2}
	l3=${#3}
	ch1=$1
	ch2=$2
	ch3=$3
	
	if [ $l1 -gt $l2 ]; then
		if [ $l1 -gt $l3 ]; then
			max=$l1
		else
			max=$l3
		fi;
	else
		if [ $l2 -gt $l3 ]; then
			max=$l2
		else
			max=$l3
		fi
	fi
	
	let "tt=$max-$l1"
	let "mid=$tt/2"
	let "res=$tt-$mid"
	for i in `seq 1 $mid`; do
		ch1=" ${ch1}"
	done;
	for i in `seq 1 $res`; do
		ch1="${ch1} "
	done;
		
	let "tt=$max-$l2"
	let "mid=$tt/2"
	let "res=$tt-$mid"
	for i in `seq 1 $mid`; do
		ch2=" ${ch2}"
	done;
	for i in `seq 1 $res`; do
		ch2="${ch2} "
	done;
	
	let "tt=$max-$l3"
	let "mid=$tt/2"
	let "res=$tt-$mid"
	for i in `seq 1 $mid`; do
		ch3=" ${ch3}"
	done;
	for i in `seq 1 $res`; do
		ch3="${ch3} "
	done;
	
	tiret="--"
	for i in `seq 1 $max`; do
		tiret=${tiret}"-"
	done;
	ch1=" "${ch1}" "
	ch2=" "${ch2}" "
	ch3=" "${ch3}" "
}

cpt $1 "#+#"
nb_pos=$res
cpt $1 "#-#"
nb_neg=$res

# adapt "abc" "abcd" "abcde"
# res dans $ch1 $ch2 $ch3

affcut="-----"
aff1="| \ |"
aff2="| + |"
aff3="| - |"

adapt "Public" "$nb_pos" "$nb_neg"
affcut=${affcut}$tiret"-"
aff1=${aff1}$ch1"|"
aff2=${aff2}$ch2"|"
aff3=${aff3}$ch3"|"

t1="Public"
t2=$nb_pos
t3=$nb_neg

for i in $(seq 1 ${#2}); do
	l=$(echo $2 | cut -c$i)
	
	cpt $1 "##$l+##"
	nb_pos=$res
	cpt $1 "##$l-##"
	nb_neg=$res

	adapt "$l" "$nb_pos" "$nb_neg"
	affcut=${affcut}$tiret"-"
	aff1=${aff1}$ch1"|"
	aff2=${aff2}$ch2"|"
	aff3=${aff3}$ch3"|"
	
	t1=$t1" "$l
	t2=$t2" "$nb_pos
	t3=$t3" "$nb_neg
done

if [ -n $3 ]; then
	fic=$3
	touch .tmp
	if [ -n $4 ] && [ `echo $4 | grep "brut" | wc -l` -ne 0 ]; then
		echo $t1>>.tmp
		echo $t2>>.tmp
		echo $t3>>.tmp
		mv .tmp $fic
	else
		echo "$affcut">>.tmp
		echo -e "$aff1">>.tmp
		echo -e "$affcut">>.tmp
		echo -e "$aff2">>.tmp
		echo -e "$aff3">>.tmp
		echo "$affcut">>.tmp
		mv .tmp $fic
	fi
else
	echo "$affcut"
	echo -e "$aff1"
	echo -e "$affcut"
	echo -e "\033[32m$aff2\033[0m"
	echo -e "\033[31m$aff3\033[0m"
	echo "$affcut"
fi