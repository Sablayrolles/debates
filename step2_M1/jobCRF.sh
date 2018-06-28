#!/bin/sh

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
	echo -e "Fail run corenlp\nBegging on $dated \n Finnishing on $datef\n\n" | mailx -v -s "[Error] Fail run corenlp" -a ~/stageM1/debates/step2\_M1/corenlp.log -a ~/stageM1/debates/step2\_M1/corenlp.err -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com >/dev/null 2>/dev/null
	exit 1
fi	

echo "Extracting EDU"
cd ~/stageM1/debates/step2_M1/
rm -f targetCRF.err 2>/dev/null
rm -f targetCRF.log 2>/dev/null
rm -f featuresCRF.log 2>/dev/null
rm -f featuresCRF.err 2>/dev/null
rm -f learnCRF.log 2>/dev/null
rm -f learnCRF.err 2>/dev/null
home=`pwd`
cd dataset
echo "python3 parse_types_annoted.py >$home/targetCRF.log 2>$home/target.err"
if [ $notifN -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	echo -e "" | mailx -v -s "[Info] Start parsing data on $datef" -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com >/dev/null 2>/dev/null
fi;
python3 parse_types_annoted.py >$home/targetCRF.log 2>$home/target.err
if [ $? -ne 0 ] && [ $notifE -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	echo -e "Fail parse types\nBegging on $dated \n Finnishing on $datef\n\n" | mailx -v -s "[Error] Fail parse types" -a $home/targetCRF.log -a $home/targetCRF.err -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com >/dev/null 2>/dev/null
	
	echo "Kill corenlp"
	pid=`ps -aux | grep "lsabalyr" | grep "java" | head -1 | awk '{print $2}'`
	kill -n 9 $pid
	
	exit 2
fi

nbFiles=`cat tmp`
echo "nbFiles="$nbFiles

cd ../features
echo "Extracting infos features"
echo "python3 saveData.py $nbFiles -c $NBCORE >>$home/featuresCRF.log 2>>$home/featuresCRF.err; echo \$?"
if [ $notifN -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	echo -e "" | mailx -v -s "[Info] Start extracting feature on $datef" -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com >/dev/null 2>/dev/null
fi;
a=`python3 saveData.py $nbFiles -c $NBCORE >$home/featuresCRF.log 2>$home/featuresCRF.err; echo $?`
if [ $a -ne 0 ] && [ $notifE -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	echo -e "Fail saveData\nBegging on $dated \n Finnishing on $datef\n\n" | mailx -v -s "[Error] Fail saveData" -a $home/featuresCRF.log -a $home/featuresCRF.err -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com >/dev/null 2>/dev/null
	
	echo "Kill corenlp"
	pid=`ps -aux | grep "lsabalyr" | grep "java" | head -1 | awk '{print $2}'`
	kill -n 9 $pid
	
	exit 3
fi
echo "Extracting features"
echo "python3 computeFeatures.py $nbFiles 2 -c $NBCORE >>$home/featuresCRF.log 2>>$home/featuresCRF.err; echo \$?"
if [ $notifN -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	echo -e "" | mailx -v -s "[Info] Start compute features on $datef" -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com >/dev/null 2>/dev/null
fi;
a=`python3 computeFeatures.py $nbFiles 2 -c $NBCORE >>$home/featuresCRF.log 2>>$home/featuresCRF.err; echo $?`
if [ $a -ne 0 ] && [ $notifE -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	echo -e "Fail computeFeatures\nBegging on $dated \n Finnishing on $datef\n\n" | mailx -v -s "[Error] Fail computeFeatures" -a $home/featuresCRF.log -a $home/featuresCRF.err -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com >/dev/null 2>/dev/null
	
	echo "Kill corenlp"
	pid=`ps -aux | grep "lsabalyr" | grep "java" | head -1 | awk '{print $2}'`
	kill -n 9 $pid
	
	exit 4
fi
echo "python3 computeFeaturesLinear.py $nbFiles 2 -p 2 -n 1 >>$home/featuresCRF.log 2>>$home/featuresCRF.err; echo \$?"
if [ $notifN -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	echo -e "" | mailx -v -s "[Info] Start compute linear features on $datef" -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com >/dev/null 2>/dev/null
fi;
a=`python3 computeFeaturesLinear.py $nbFiles 2 -p 2 -n 1  >>$home/featuresCRF.log 2>>$home/featuresCRF.err; echo $?`
if [ $a -ne 0 ] && [ $notifE -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	echo -e "Fail computeFeaturesLinear\nBegging on $dated \n Finnishing on $datef\n\n" | mailx -v -s "[Error] Fail computeFeaturesLinear" -a $home/featuresCRF.log -a $home/featuresCRF.err -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com >/dev/null 2>/dev/null
	
	echo "Kill corenlp"
	pid=`ps -aux | grep "lsabalyr" | grep "java" | head -1 | awk '{print $2}'`
	kill -n 9 $pid
	
	exit 4
fi

cd ../learning
echo "Learning"
echo "python3 crf.py $nbFiles >>$home/learnCRF.log 2>>$home/learnCRF.err; echo \$?"
echo "File of plotting : scrs"
if [ $notifN -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	echo -e "" | mailx -v -s "[Info] Start learning on $datef" -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com >/dev/null 2>/dev/null
fi;
echo "Setting crontab"
echo '* * * * * python3 '$home'/learning/plot3d.py && echo -e "Plot crf\n" | mailx -v -s "[Info] Plot crf" -a '$home'/learning/graph.png -a '$home'/learnCRF.err -a '$home'/learnCRF.log -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com'>./cron
crontab ./cron
rm ./cron
a=`python3 crf.py $nbFiles >>$home/learnCRF.log 2>>$home/learnCRF.err; echo $?`
if [ $a -ne 0 ] && [ $notifE -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	echo -e "Fail crf\nBegging on $dated \n Finnishing on $datef\n\n" | mailx -v -s "[Error] Fail crf" -a $home/learnCRF.log -a $home/learnCRF.err -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com >/dev/null 2>/dev/null
	
	echo "Del crontab"
	crontab -r
	echo "Kill corenlp"
	pid=`ps -aux | grep "lsabalyr" | grep "java" | head -1 | awk '{print $2}'`
	kill -n 9 $pid

	exit 5
fi
echo "Del crontab"
crontab -r
echo "Kill corenlp"
pid=`ps -aux | grep "lsabalyr" | grep "java" | head -1 | awk '{print $2}'`
kill -n 9 $pid

#send result by mail
if [ $notifS -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	res=`cat $home/learning/res`
	echo -e "Result learning finish\nBegging on $dated \n Finnishing on $datef\n\n $res" | mailx -v -s "[Result] Result learning" -a $home/targetCRF.log -a $home/targetCRF.err -a $home/featuresCRF.log -a $home/featuresCRF.err -a $home/learnCRF.log -a $home/learnCRF.err -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com >/dev/null 2>/dev/null
fi;