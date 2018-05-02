#!/bin/bash

echo -e "Usage : $0 \n"

if [ ! -f ./config_old.txt ]; then
	echo "Nothing to harmonise"
	exit 0
fi;

old_date=`head -1 ./config_old.txt`
old_brut=`head -2 ./config_old.txt | tail -1 | cut -d\; -f2`
old_segmented=`head -3 ./config_old.txt | tail -1 | cut -d\; -f2`
old_full=`head -4 ./config_old.txt | tail -1 | cut -d\; -f2`
old_reaction=`head -5 ./config_old.txt | tail -1 | cut -d\; -f2`

date=`head -1 ./config.txt`
brut=`head -2 ./config.txt | tail -1 | cut -d\; -f2`
segmented=`head -3 ./config.txt | tail -1 | cut -d\; -f2`
full=`head -4 ./config.txt | tail -1 | cut -d\; -f2`
reaction=`head -5 ./config.txt | tail -1 | cut -d\; -f2`

for dos in `ls -d ./*/ | grep -v "scripts"`; do
	dos=${dos:2:${#dos}-3}
	echo "country : $dos"
	for year in `ls -d ./$dos/*/`; do
		year=${year:2:${#year}-3}
		year=`basename $year`
		echo -e "\tfor year : $year"
		for debate in `ls -d ./$dos/$year/*/`; do
			debate=${debate:2:${#debate}-3}
			debate=`basename $debate`
			echo -e "\t\tdebate $debate OK"
			mv ./$dos/$year/$debate/$old_brut ./$dos/$year/$debate/$brut 2>/dev/null
			mv ./$dos/$year/$debate/$old_segmented ./$dos/$year/$debate/$segmented 2>/dev/null
			mv ./$dos/$year/$debate/$old_full ./$dos/$year/$debate/$full 2>/dev/null
			mv ./$dos/$year/$debate/$old_reaction ./$dos/$year/$debate/$reaction 2>/dev/null
		done;
	done;
done;
rm ./config_old.txt
echo "all is harmonise"
exit 0