#!/bin/bash

echo "Usage : $0 [H|S|c] num_method_1,...,num_method_n lambda_1,...,lambda_n PATH_CORPUS \"NOM_DES_CANDIDATS\" name_fic_result"
echo "H : hand parsed"
echo "S : script parsed"
echo "c : get and save the contributions"
echo 'exemple : ./scripts/notations/get_scoring.sh H 2,3 1,0.99,0.98,0.97,0.96,0.95,0.9,0.85,0.8,0.75,0.7 ./usa/2016/1/ "TRUMP CLINTON" res_scoring'

LOCATE="./scripts/notations/evaluate_note_v1.py"
PARAMETER="-m"
MAX_ARGS=6
MIN_ARGS=5

NOT_ENOUGH_PARAMETERS=1
WRONG_ARGUMENTS=2


if [ $# -lt $MIN_ARGS -o $# -gt $MAX_ARGS ]; then
	echo "Not enough parameters"
	exit $NOT_ENOUGH_PARAMETERS
fi;

test=`echo "$1" | grep -E "(H|S|c)"`
if [  $# -eq $MAX_ARGS -a "$test" != "$1" ]; then
	exit $WRONG_ARGUMENTS
fi;
PARAMETER="$PARAMETER"$1

if [ $# -eq $MAX_ARGS ]; then
	methods=$2
	lambdas=$3
	corpus=$4
	names=$5
	result=$6
else
	methods=$1
	lambdas=$2
	corpus=$3
	names=$4
	result=$5
fi

if [ `echo $methods | grep "," | wc -l` -ne 0 ]; then
	nbM=1
	cmd=`echo $methods | cut -d\, -f$nbM`
	while [ "$cmd" != "" ]; do
		let "nbM=$nbM+1"
		cmd=`echo $methods | cut -d\, -f$nbM`
	done;
	let "nbM=$nbM-1"
else
	nbM=1
	methods=$methods","
fi
if [ `echo $lambdas | grep "," | wc -l` -ne 0 ]; then
	nbL=1
	cmd=`echo $lambdas | cut -d\, -f$nbL`
	while [ "$cmd" != "" ]; do
		let "nbL=$nbL+1"
		cmd=`echo $lambdas | cut -d\, -f$nbL`
	done;
	let "nbL=$nbL-1"
else
	nbL=1
	lambdas=$lambdas","
fi
if [ `echo $names | grep " " | wc -l` -ne 0 ]; then
	nbN=1
	cmd=`echo $names | cut -d' ' -f$nbN`
	while [ "$cmd" != "" ]; do
		let "nbN=$nbN+1"
		cmd=`echo $names | cut -d' ' -f$nbN`
	done;
	let "nbN=$nbN-1"
else
	nbN=1
	names=$names" "
fi
met=1
rm res 2>/dev/null
echo ""
echo ""
touch res
echo "(method,name,lambda,score)">>res
while [ $met -le $nbM ]; do
	method=`echo $methods | cut -d\, -f$met`
	echo "Method $method"
	nam=1
	while [ $nam -le $nbN ]; do
		name=`echo $names | cut -d" " -f$nam`
		echo -e "\tName: $name"
		lamb=1
		while [ $lamb -le $nbL ]; do
			lambda=`echo $lambdas | cut -d\, -f$lamb`
			echo -e "\t\tLambda : $lambda"
			p=$PARAMETER"M"$method"L"$lambda
			nameFic="M"$method"L"$lambda".result"
			nameFic2="M"$method"L"$lambda".contrib"
			if [ ! -f $nameFic ]; then
				#echo "$LOCATE $p $corpus >fic"
				cmd=`$LOCATE $p $corpus >fic`;
				cmd=`cat fic | grep "^M" >$nameFic2`
				cmd=`sed -i -e "s/'//g" fic`;
				cmd=`sed -i -e "s/{//g" fic`;
				cmd=`sed -i -e "s/}//g" fic`;
				cmd=`sed -i -e "s/\,/\n/g" fic`;
				cmd=`sed -i -e "s/ //g" fic`
			else
				# echo "Using $nameFic"
				cp $nameFic fic
			fi
			score=`cat fic | grep "$name" | cut -d\: -f2`
			echo -e "\t\t\tScore:$score"
			if [ ! -f $nameFic	]; then
				mv fic $nameFic
			fi;
			echo "($method,$name,$lambda,$score)" >>res
			let "lamb=$lamb+1"
		done;
		let "nam=$nam+1"
	done;
	echo "" >>res
	let "met=$met+1"
done;

date=`date "+%d_%m-%H_%M"`

dataset=`echo $corpus | sed "s/\.\//_/g" | sed "s/\//_/g"`

mv res ./scripts/notations/result/scores/$result"_"$date"_"$dataset
rm *.result 2>/dev/null
rm fic 2>/dev/null

test=`echo "$1" | grep "c"`
if [  $# -eq $MAX_ARGS -a "$test" != "$1" ]; then
	rm *.contrib 2>/dev/null
fi;

echo "Results on"
echo "./scripts/notations/result/scores/"$result"_"$date"_"$dataset