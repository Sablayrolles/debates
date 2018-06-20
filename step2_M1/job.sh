#!/bin/sh

echo "Usage : $0 -[esn0]"
echo "-e : Send email when error"
echo "-s : Send email when success"
echo "-n : Send email after each step"
echo "-0 : No notification"
echo "default : -es"

notifE=1
notifS=1
notifN=0

if [ -n $1 ] && [ `echo $1 | grep "n" | wc -l` -eq 1 ]; then
	notifN=1
fi;

if [ -n $1 ] && [ `echo $1 | grep "0" | wc -l` -eq 1 ]; then
	notifE=0
	notifS=0
	notifN=0
fi;


dated=`date "+%y/%m/%d %H:%M:%S"`
echo "Running java corenlp"
cd ~/stageM1/corenlp/
./run.sh >~/stageM1/debates/step2\_M1/corenlp.log 2>~/stageM1/debates/step2\_M1/corenlp.err &
if [ $? -ne 0 ] && [ $notifE -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	echo -e "Fail run corenlp\nBegging on $dated \n Finnishing on $datef\n\n" | mailx -v -s "[Error] Fail run corenlp" -a ~/stageM1/debates/step2\_M1/corenlp.log -a ~/stageM1/debates/step2\_M1/corenlp.err -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com
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
if [ $notifN -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	echo -e "" | mailx -v -s "[Info] Start parsing data on $datef" -a $home/target.log -a $home/target.err -a $home/features.log -a $home/features.err -a $home/learn.log -a $home/learn.err -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com
fi;
python3 parse_types_annoted.py >$home/target.log 2>$home/target.err
if [ $? -ne 0 ] && [ $notifE -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	echo -e "Fail parse types\nBegging on $dated \n Finnishing on $datef\n\n" | mailx -v -s "[Error] Fail parse types" -a $home/target.log -a $home/target.err -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com
	
	echo "Kill corenlp"
	pid=`ps -aux | grep "lsabalyr" | grep "java" | head -1 | awk '{print $2}'`
	kill -9 $pid
	
	exit 2
fi

nbFiles=`cat tmp`
echo "nbFiles="$nbFiles

cd ../features
echo "Extracting infos features"
echo "python3 saveData.py $nbFiles >>$home/features.log 2>>$home/features.err; echo \$?"
if [ $notifN -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	echo -e "" | mailx -v -s "[Info] Start extracting feature on $datef" -a $home/target.log -a $home/target.err -a $home/features.log -a $home/features.err -a $home/learn.log -a $home/learn.err -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com
fi;
a=`python3 saveData.py $nbFiles >$home/features.log 2>$home/features.err; echo $?`
if [ $a -ne 0 ] && [ $notifE -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	echo -e "Fail saveData\nBegging on $dated \n Finnishing on $datef\n\n" | mailx -v -s "[Error] Fail saveData" -a $home/features.log -a $home/features.err -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com
	
	echo "Kill corenlp"
	pid=`ps -aux | grep "lsabalyr" | grep "java" | head -1 | awk '{print $2}'`
	kill -9 $pid
	
	exit 3
fi
echo "Extracting features"
echo "python3 computeFeatures.py $nbFiles >>$home/features.log 2>>$home/features.err; echo \$?"
if [ $notifN -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	echo -e "" | mailx -v -s "[Info] Start compute features on $datef" -a $home/target.log -a $home/target.err -a $home/features.log -a $home/features.err -a $home/learn.log -a $home/learn.err -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com
fi;
a=`python3 computeFeatures.py $nbFiles >>$home/features.log 2>>$home/features.err; echo $?`
if [ $a -ne 0 ] && [ $notifE -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	echo -e "Fail computeFeatures\nBegging on $dated \n Finnishing on $datef\n\n" | mailx -v -s "[Error] Fail computeFeatures" -a $home/features.log -a $home/features.err -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com
	
	echo "Kill corenlp"
	pid=`ps -aux | grep "lsabalyr" | grep "java" | head -1 | awk '{print $2}'`
	kill -9 $pid
	
	exit 4
fi

cd ../learning
echo "Learning"
echo "python3 logistic_reg.py $nbFiles >>$home/learn.log 2>>$home/learn.err; echo \$?"
if [ $notifN -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	echo -e "" | mailx -v -s "[Info] Start learning on $datef" -a $home/target.log -a $home/target.err -a $home/features.log -a $home/features.err -a $home/learn.log -a $home/learn.err -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com
fi;
a=`python3 logistic_reg.py $nbFiles >>$home/learn.log 2>>$home/learn.err; echo $?`
if [ $a -ne 0 ] && [ $notifE -eq 1 ]; then
	datef=`date "+%y/%m/%d %H:%M:%S"`
	echo -e "Fail logistic_reg\nBegging on $dated \n Finnishing on $datef\n\n" | mailx -v -s "[Error] Fail logistic_reg" -a $home/learn.log -a $home/learn.err -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com
	
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
	res=`cat learning/res`
	echo -e "Result learning finish\nBegging on $dated \n Finnishing on $datef\n\n $res" | mailx -v -s "[Result] Result learning" -a $home/target.log -a $home/target.err -a $home/features.log -a $home/features.err -a $home/learn.log -a $home/learn.err -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com
fi;