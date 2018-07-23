#!/bin/sh

echo "Setting crontab"

#plot 1h
echo '0 * * * * python3 ~/stageM1/debates/step2\_M1/learning/plot3d.py >/dev/null 2>/dev/null ; echo "Plot crf  --   " | mailx -v -s "[Info] Plot crf" -a ~/graph.png -a ~/accuracies_c1.png -a ~/accuracies_c2.png -a ~/accuracies_maxiter.png -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com >>~/logs/mailx.log 2>~/logs/mailx.err'>./cron

#files 3h
echo '0 0,3,6,9,12,15,18,21 * * * python3 ~/stageM1/debates/step2\_M1/learning/plot3d.py >/dev/null 2>/dev/null ; echo "Plot crf  --   " | mailx -v -s "[Info] Plot crf" -a ~/stageM1/debates/step2\_M1/learnCRF.err -a ~/stageM1/debates/step2\_M1/learnCRF.log -S smtp-use-starttls -S ssl-verify=ignore -S smtp-auth=login -S smtp=smtp://smtp.gmail.com:587 -S from="louis.sablayrolles@gmail.com(Sablayrolles Louis)" -S smtp-auth-user=louis.sablayrolles@gmail.com -S smtp-auth-password=eragon1996 -S ssl-verify=ignore -S nss-config-dir=~/.certs louis.sablayrolles@gmail.com >>~/logs/mailx.log 2>~/logs/mailx.err'>./cron
crontab ./cron
rm ./cron