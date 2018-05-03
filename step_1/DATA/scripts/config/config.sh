#!/bin/bash

echo "Don't end all your path with / and don't begin with ./"
read -p "Path of the rep brut files from all corpus : " brut
read -p "Path of the rep hand segmented files from all corpus : " segmented
read -p "Path of the rep full files from all corpus : " full
read -p "Path of the rep reaction files from all corpus :" reaction

if [ -f ./config.txt ]; then
	mv ./config.txt ./config_old.txt
fi;

date=`date "+%d_%m-%H_%M"`

echo -e "$date">./config.txt
echo -e "Brut;$brut">>./config.txt
echo -e "Segmented;$segmented">>./config.txt
echo -e "Full;$full">>./config.txt
echo -e "Reaction;$reaction">>./config.txt

echo -e "Configuration ended\n Should apply harmonise_config.sh"
exit 0
