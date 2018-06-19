#!/bin/sh

echo "Running java corenlp"
cd ~/stageM1/corenlp/
./run.sh >~/stageM1/debates/step2\_M1/corenlp.log 2>~/stageM1/debates/step2\_M1/corenlp.err

echo "Extracting EDU"
cd ~/stageM1/debates/step2_M1/
home=`pwd`
cd dataset
python3 parse_types_annoted.py >$home/job.log 2>$home/job.err

nbFiles=`cat tmp`
echo "nbFiles="$nbFiles

cd ../features
echo "Extracting infos features"
echo "python3 saveData.py $nbFiles >>$home/job.log 2>>$home/job.err"
a=`python3 saveData.py $nbFiles >>$home/job.log 2>>$home/job.err`
echo "Extracting features"
echo "python3 computeFeatures.py $nbFiles >>$home/job.log 2>>$home/job.err"
a=`python3 computeFeatures.py $nbFiles >>$home/job.log 2>>$home/job.err`

cd ../learning
echo "Learning"
echo "python3 logistic_reg.py $nbFiles >>$home/job.log 2>>$home/job.err"
a=`python3 logistic_reg.py $nbFiles >>$home/job.log 2>>$home/job.err`

#send result by mail
date=`date "+%y/%m/%d %H:%M:%S"`
echo -e "Result learning finish on $date" | mailx -v -s "Result learning" -a $home/job.log -a $home/job.err -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com
