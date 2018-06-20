#!/bin/sh

dated=`date "+%y/%m/%d %H:%M:%S"`
echo "Running java corenlp"
cd ~/stageM1/corenlp/
./run.sh >~/stageM1/debates/step2\_M1/corenlp.log 2>~/stageM1/debates/step2\_M1/corenlp.err

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
python3 parse_types_annoted.py >$home/target.log 2>$home/target.err

nbFiles=`cat tmp`
echo "nbFiles="$nbFiles

cd ../features
echo "Extracting infos features"
echo "python3 saveData.py $nbFiles >>$home/job.log 2>>$home/job.err"
a=`python3 saveData.py $nbFiles >$home/features.log 2>$home/features.err`
echo "Extracting features"
echo "python3 computeFeatures.py $nbFiles >>$home/job.log 2>>$home/job.err"
a=`python3 computeFeatures.py $nbFiles >>$home/features.log 2>>$home/features.err`

cd ../learning
echo "Learning"
echo "python3 logistic_reg.py $nbFiles >>$home/job.log 2>>$home/job.err"
a=`python3 logistic_reg.py $nbFiles >>$home/learn.log 2>>$home/learn.err`

#send result by mail
datef=`date "+%y/%m/%d %H:%M:%S"`
echo -e "Result learning finish\nBegging on $dated \n Finnishing on $datef\n" | mailx -v -s "Result learning" -a $home/target.log -a $home/target.err -a $home/features.log -a $home/features.err -a $home/learn.log -a $home/learn.err -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com
