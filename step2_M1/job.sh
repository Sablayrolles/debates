#!/bin/sh

#pour focntion sendMail
source ~/.bash_profile

echo "\nUsage : $0 -[esv0] [-c NBCORE]"
echo "-e : Send email when error"
echo "-s : Send email when success"
echo "-v : Send email after each step(verbose)"
echo "-0 : No notification"
echo -e "default : -ens -c 7\n\n"

notifE=1
notifS=1
notifN=1
NBCORE=7

if [ -n $1 ]; then	
	if [ `echo $1 | grep "v" | wc -l` -eq 1 ]; then
		notifN=1
		notifE=0
		notifS=0
	fi;
	
	if [ `echo $1 | grep "s" | wc -l` -eq 1 ]; then
		notifS=1
		notifN=0
		notifE=0
	fi;
	
	if [ `echo $1 | grep "e" | wc -l` -eq 1 ]; then
		notifE=1
		notifS=0
		notifN=0
	fi;
	
	if [ `echo $1 | grep "0" | wc -l` -eq 1 ]; then
		notifE=0
		notifS=0
		notifN=0
	fi;
	if [ `echo $1 | grep "c" | wc -l` -eq 1 ]; then
		if [ -n $2 ]; then
			NBCORE=$2
		fi;
	fi;
fi;

echo -e "NBCORE"$NBCORE"\nNotification error:"$notifE"\nNotification success:"$notifS"\nNotification step:"$notifN

rm -f corenlp.err 2>/dev/null
rm -f corenlp.log 2>/dev/null

dated=`date "+%y/%m/%d %H:%M:%S"`
echo "Running java corenlp"
cd ~/stageM1/corenlp/
./run.sh >>~/stageM1/debates/step2\_M1/corenlp.log 2>>~/stageM1/debates/step2\_M1/corenlp.err &
if [ $? -ne 0 ] && [ $notifE -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	sendMail louis.sablayrolles@gmail.com "[Error] Fail run corenlp" "Fail run corenlp\nBegging on $dated \n Finnishing on $datef\n\n" ~/stageM1/debates/step2\_M1/corenlp.log ~/stageM1/debates/step2\_M1/corenlp.err
	exit 1
fi	

echo "Extracting EDU"
cd ~/stageM1/debates/step2_M1/
rm -f target.err 2>/dev/null
rm -f target.log 2>/dev/null
rm -f features.log 2>/dev/null
rm -f features.err 2>/dev/null
rm -f job.log 2>/dev/null
rm -f job.err 2>/dev/null
home=`pwd`
cd dataset
echo "python3 parse_types_annoted.py >$home/target.log 2>$home/target.err"
if [ $notifN -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	sendMail louis.sablayrolles@gmail.com "[Info] Start parsing data on $datef" " "
fi;
python3 parse_types_annoted.py >$home/target.log 2>$home/target.err
if [ $? -ne 0 ] && [ $notifE -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	sendMail louis.sablayrolles@gmail.com "[Error] Fail parse types" "Fail parse types\nBegging on $dated \n Finnishing on $datef\n\n" ~/stageM1/debates/step2\_M1/target.log ~/stageM1/debates/step2\_M1/target.err
	
	echo "Kill corenlp"
	pid=`ps -aux | grep "lsabalyr" | grep "java" | head -1 | awk '{print $2}'`
	kill -9 $pid
	
	exit 2
fi

nbFiles=`cat tmp`
echo "nbFiles="$nbFiles

cd ../features
echo "Extracting infos features"
echo "python3 saveData.py $nbFiles -c $NBCORE >>$home/features.log 2>>$home/features.err; echo \$?"
if [ $notifN -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	sendMail louis.sablayrolles@gmail.com "[Info] Start extracting feature on $datef" " " 
fi;
a=`python3 saveData.py $nbFiles -c $NBCORE >$home/features.log 2>$home/features.err; echo $?`
if [ $a -ne 0 ] && [ $notifE -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	sendMail louis.sablayrolles@gmail.com "[Error] Fail saveData" "Fail saveData\nBegging on $dated \n Finnishing on $datef\n\n" ~/stageM1/debates/step2\_M1/features.log ~/stageM1/debates/step2\_M1/features.err
	
	echo "Kill corenlp"
	pid=`ps -aux | grep "lsabalyr" | grep "java" | head -1 | awk '{print $2}'`
	kill -9 $pid
	
	exit 3
fi
echo "Extracting features"
echo "python3 computeFeatures.py $nbFiles 1 -c $NBCORE >>$home/features.log 2>>$home/features.err; echo \$?"
if [ $notifN -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	sendMail louis.sablayrolles@gmail.com "[Info] Start compute features on $datef" " "
fi;
a=`python3 computeFeatures.py $nbFiles 1 -c $NBCORE >>$home/features.log 2>>$home/features.err; echo $?`
if [ $a -ne 0 ] && [ $notifE -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	sendMail louis.sablayrolles@gmail.com "[Error] Fail computeFeatures" "Fail computeFeatures\nBegging on $dated \n Finnishing on $datef\n\n" ~/stageM1/debates/step2\_M1/features.log ~/stageM1/debates/step2\_M1/features.err
	
	echo "Kill corenlp"
	pid=`ps -aux | grep "lsabalyr" | grep "java" | head -1 | awk '{print $2}'`
	kill -9 $pid
	
	exit 4
fi
echo "python3 computeFeaturesLinear.py $nbFiles 1 -p 2 -n 1 >>$home/features.log 2>>$home/features.err; echo \$?"
if [ $notifN -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	sendMail louis.sablayrolles@gmail.com "[Info] Start compute linear features on $datef" " "
fi;
a=`python3 computeFeaturesLinear.py $nbFiles 1 -p 2 -n 1  >>$home/features.log 2>>$home/features.err; echo $?`
if [ $a -ne 0 ] && [ $notifE -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	sendMail louis.sablayrolles@gmail.com "[Error] Fail computeFeaturesLinear" "Fail computeFeaturesLinear\nBegging on $dated \n Finnishing on $datef\n\n" ~/stageM1/debates/step2\_M1/features.log ~/stageM1/debates/step2\_M1/features.err
	
	echo "Kill corenlp"
	pid=`ps -aux | grep "lsabalyr" | grep "java" | head -1 | awk '{print $2}'`
	kill -9 $pid
	
	exit 4
fi

cd ../learning
echo "Learning"
echo "python3 logistic_reg.py $nbFiles -c $NBCORE >>$home/learn.log 2>>$home/learn.err; echo \$?"
if [ $notifN -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	sendMail louis.sablayrolles@gmail.com "[Info] Start learning on $datef" " "
fi;
a=`python3 logistic_reg.py $nbFiles -c $NBCORE >>$home/learn.log 2>>$home/learn.err; echo $?`
if [ $a -ne 0 ] && [ $notifE -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	sendMail louis.sablayrolles@gmail.com "[Error] Fail logistic_reg" "Fail logistic_reg\nBegging on $dated \n Finnishing on $datef\n\n" ~/stageM1/debates/step2\_M1/learn.log ~/stageM1/debates/step2\_M1/learn.err
	
	echo "Kill corenlp"
	pid=`ps -aux | grep "lsabalyr" | grep "java" | head -1 | awk '{print $2}'`
	kill -9 $pid

	exit 5
fi

echo "Kill corenlp"
pid=`ps -aux | grep "lsabalyr" | grep "java" | head -1 | awk '{print $2}'`
kill -9 $pid

#send result by mail
if [ $notifS -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	res=`cat $home/learning/res`
	sendMail louis.sablayrolles@gmail.com "[Result] Result learning" "Result learning finish\nBegging on $dated \n Finnishing on $datef\n\n $res" ~/stageM1/debates/step2\_M1/target.log ~/stageM1/debates/step2\_M1/target.err ~/stageM1/debates/step2\_M1/features.log ~/stageM1/debates/step2\_M1/features.err ~/stageM1/debates/step2\_M1/learn.log ~/stageM1/debates/step2\_M1/learn.err
fi;